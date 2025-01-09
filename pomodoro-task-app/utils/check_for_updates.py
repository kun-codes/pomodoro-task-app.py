from http.client import HTTPSConnection
from urllib.parse import urlparse
import ssl
import certifi

import tomllib
from constants import UPDATE_CHECK_URL, UpdateCheckResult
from loguru import logger
from utils.get_app_version import get_app_version


def checkForUpdates():
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
            if e.errno == 101:  # Network unreachable error
                raise ConnectionError("Network is unreachable")
            raise e  # Re-raise other OSErrors

        response = conn.getresponse()

        if response.status != 200:
            raise Exception(f"HTTP error occurred: {response.status} {response.reason}")

        remote_pyproject = tomllib.loads(response.read().decode("utf-8"))
        remote_app_version = remote_pyproject["tool"]["poetry"]["version"]

        if remote_app_version > current_app_version:
            logger.warning(f"New version available: {remote_app_version}")
            return UpdateCheckResult.UPDATE_AVAILABLE
        else:
            logger.debug("App is up to date")
            return UpdateCheckResult.UP_TO_DATE

    except ConnectionError:
        logger.error("Failed to check for updates: Network is unreachable")
        return UpdateCheckResult.NETWORK_UNREACHABLE
    except Exception as err:
        logger.error(f"An error occurred: {err}")
        return UpdateCheckResult.UNKNOWN_ERROR
    finally:
        if "conn" in locals():
            conn.close()
