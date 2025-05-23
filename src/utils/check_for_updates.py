import ssl
from http.client import HTTPSConnection
from urllib.parse import urlparse
from typing import Callable, Optional
from PySide6.QtCore import QThread, Signal, QObject

import certifi
import tomllib
from loguru import logger
from semver import Version

from constants import UPDATE_CHECK_URL, UpdateCheckResult
from utils.get_app_version import get_app_version


class UpdateChecker(QObject):
    """A thread-based update checker that doesn't block the GUI."""
    updateCheckComplete = Signal(UpdateCheckResult)

    def __init__(self):
        super().__init__()
        self._thread = QThread()
        self.moveToThread(self._thread)
        self._thread.started.connect(self._check_for_updates)

    def start(self):
        """Start the update check in a separate thread."""
        self._thread.start()

    def _check_for_updates(self):
        """Internal method that performs the actual update check."""
        result = self.checkForUpdates()
        self.updateCheckComplete.emit(result)
        self._thread.quit()

    @staticmethod
    def checkForUpdates():
        """Check for updates by comparing the current app version with the remote version."""
        current_app_version = get_app_version()
        logger.debug(f"App version: {current_app_version}")

        parsed_url = urlparse(UPDATE_CHECK_URL)

        try:
            # Create SSL context with certifi - works on all platforms
            context = ssl.create_default_context(cafile=certifi.where())
            conn = HTTPSConnection(parsed_url.netloc, context=context)
            try:
                conn.request("GET", parsed_url.path)
            except OSError as e:
                if e.errno in [101, -3, 110, 111, 113]:  # Handle specific network-related errors
                    raise ConnectionError(f"Network error occurred: {e.strerror}")
                raise e  # Re-raise other OSErrors

            response = conn.getresponse()

            if response.status != 200:
                raise Exception(f"HTTP error occurred: {response.status} {response.reason}")

            remote_pyproject = tomllib.loads(response.read().decode("utf-8"))
            remote_app_version = remote_pyproject["tool"]["poetry"]["version"]

            # Convert versions to semver Version instances for proper comparison
            current_ver = Version.parse(current_app_version)
            remote_ver = Version.parse(remote_app_version)

            if remote_ver > current_ver:
                logger.warning(f"New version available: {remote_app_version}")
                return UpdateCheckResult.UPDATE_AVAILABLE
            else:
                logger.debug("App is up to date")
                return UpdateCheckResult.UP_TO_DATE

        except ConnectionError as conn_err:
            logger.error(f"Failed to check for updates: {conn_err}")
            return UpdateCheckResult.NETWORK_UNREACHABLE
        except Exception as err:
            logger.error(f"An error occurred: {err}")
            return UpdateCheckResult.UNKNOWN_ERROR
        finally:
            if "conn" in locals():
                conn.close()
