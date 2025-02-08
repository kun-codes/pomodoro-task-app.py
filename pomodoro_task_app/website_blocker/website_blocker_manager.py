import os
import shlex
import shutil
import subprocess
import threading

from loguru import logger
from PySide6.QtCore import QObject
from uniproxy import Uniproxy

from config_values import ConfigValues
from constants import MITMDUMP_COMMAND_LINUX, MITMDUMP_COMMAND_WINDOWS, MITMDUMP_SHUTDOWN_URL
from utils.noHTTPClientError import NoHTTPClientError
from website_blocker.utils import kill_process


class WebsiteBlockerManager(QObject):
    def __init__(self):
        super().__init__()
        self.proxy = Uniproxy("127.0.0.1", ConfigValues.PROXY_PORT)

    def start_filtering(
        self,
        listening_port: int,
        joined_addresses: str,
        block_type: str,
        mitmdump_bin_path: str,
    ):
        """Function which starts filtering."""
        logger.debug("Inside WebsiteBLockerManager.start_filtering().")

        self.stop_filtering(delete_proxy=False)

        # self.proxy.join()
        threading.Thread(target=self.proxy.join).start()

        # Start mitmdump, passing filter.py.
        # if windows then
        if os.name == "nt":
            args = shlex.split(
                MITMDUMP_COMMAND_WINDOWS.format(mitmdump_bin_path, listening_port, joined_addresses, block_type),
                posix=False,
            )
        else:
            args = shlex.split(
                MITMDUMP_COMMAND_LINUX.format(mitmdump_bin_path, listening_port, joined_addresses, block_type)
            )
        subprocess.Popen(args)

    def stop_filtering(self, delete_proxy: bool = True):
        logger.debug("Inside WebsiteBlockerManager.stop_filtering().")

        if delete_proxy:
            threading.Thread(target=self.proxy.delete_proxy).start()

        try:
            # detect if curl is installed
            curl_path = shutil.which("curl")
            # detect if wget is installed
            wget_path = shutil.which("wget")

            null_device = "NUL" if os.name == "nt" else "/dev/null"

            if curl_path:
                result = subprocess.run(
                    [curl_path, "-s", "--proxy", f"127.0.0.1:{ConfigValues.PROXY_PORT}", MITMDUMP_SHUTDOWN_URL]
                )
                logger.debug(f"curl command return code: {result.returncode}")
                if result.returncode == 7:
                    logger.debug("curl return code 7: Most likely mitmproxy/mitmdump isn't running")
            elif wget_path:
                # https://askubuntu.com/a/586550
                result = subprocess.run([
                    wget_path,
                    "-q",  # quiet mode
                    "-O", null_device,  # discard output file
                    "-e", "use_proxy=yes",
                    "-e", f"http_proxy=http://127.0.0.1:{ConfigValues.PROXY_PORT}",
                    MITMDUMP_SHUTDOWN_URL
                ])
                logger.debug(f"wget command return code: {result.returncode}")
                if result.returncode == 4:
                    logger.debug("wget return code 4: Most likely mitmproxy/mitmdump isn't running")
            else:
                raise NoHTTPClientError("Neither curl nor wget found.")
        except Exception as e:
            logger.error(f"Graceful shutdown of mitmdump failed: {e}")
            # Fall back to force kill if graceful shutdown fails
            logger.info("Falling back to force kill of mitmdump and mitmproxy.")
            kill_process()
