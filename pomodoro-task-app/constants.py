import sys
from enum import Enum
import os
from pathlib import Path

# Application
ORGANIZATION_NAME = "Pomodoro App"
APPLICATION_NAME = "Pomodoro"

# for pomodoro timer of new workspaces
WORK_DURATION = 25
BREAK_DURATION = 5
LONG_BREAK_DURATION = 15
WORK_INTERVALS = 2
AUTOSTART_WORK = True
AUTOSTART_BREAK = True
ENABLE_WEBSITE_FILTER = True

MITMDUMP_COMMAND_LINUX = '{} --set allow_remote=true --showhost -s {} --set "addresses_str={}" --set "block_type={}"'.format(
    '{}', os.path.join(getattr(sys, '_MEIPASS', Path(__file__).parent), 'website_blocker', 'filter.py'), '{}', '{}'
)  # using _MEIPASS to make it compatible with pyinstaller
# the os.path.join returns the location of filter.py

MITMDUMP_COMMAND_WINDOWS = r'{} --set allow_remote=true --showhost -s {} --set addresses_str={} --set block_type={}'.format(
    '{}', os.path.join(getattr(sys, '_MEIPASS', Path(__file__).parent), 'website_blocker', 'filter.py'), '{}', '{}'
)  # using _MEIPASS to make it compatible with pyinstaller
# the os.path.join returns the location of filter.py

BLOCK_HTML_MESSAGE = f"<h1>Website blocked by {APPLICATION_NAME}!</h1>"

class WebsiteFilterType(Enum):
    BLOCKLIST = 0
    ALLOWLIST = 1


class URLListType(Enum):
    BLOCKLIST = "blocklist_urls"
    BLOCKLIST_EXCEPTION = "blocklist_exception_urls"
    ALLOWLIST = "allowlist_urls"
    ALLOWLIST_EXCEPTION = "allowlist_exception_urls"
