import os
import shlex
import subprocess
import threading

from loguru import logger
from PySide6.QtCore import QObject
from uniproxy import Uniproxy

from config_values import ConfigValues
from constants import MITMDUMP_COMMAND_LINUX, MITMDUMP_COMMAND_WINDOWS
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
            kill_process()
        # In case there are no mitmproxy processes open.
        except:
            pass
