import os

from PySide6.QtCore import QObject
from website_blocker.utils import kill_process
from uniproxy import Uniproxy
from constants import MITMDUMP_COMMAND_LINUX
from loguru import logger
import subprocess
import shlex

class WebsiteBlockerManager(QObject):
    def __init__(self):
        super().__init__()
        self.proxy = Uniproxy("127.0.0.1", 8080)

    def start_filtering(self, listening_port: int, joined_addresses: str, block_type: str,
                    mitmdump_bin_path: str,):
        """Function which starts filtering."""
        logger.debug("Inside WebsiteBLockerManager.start_filtering().")

        self.stop_filtering()

        self.proxy.join()

        # Start mitmdump, passing filter.py.
        # if windows then
        if os.name == 'nt':
            args = shlex.split(MITMDUMP_COMMAND_LINUX.format(mitmdump_bin_path,
                                                               joined_addresses,
                                                               block_type), posix=False)
        else:
            args = shlex.split(MITMDUMP_COMMAND_LINUX.format(mitmdump_bin_path,
                                                   joined_addresses,
                                                   block_type))
        mitmdump = subprocess.Popen(args)

    def stop_filtering(self):
        logger.debug("Inside WebsiteBlockerManager.stop_filtering().")
        self.proxy.delete_proxy()
        try:
            kill_process()
        # In case there are no mitmproxy processes open.
        except:
            pass
