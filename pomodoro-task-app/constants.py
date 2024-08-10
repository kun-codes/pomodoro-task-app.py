from enum import Enum

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


class WebsiteFilterType(Enum):
    BLOCKLIST = 0
    ALLOWLIST = 1


class URLListType(Enum):
    BLOCKLIST = "blocklist_urls"
    BLOCKLIST_EXCEPTION = "blocklist_exception_urls"
    ALLOWLIST = "allowlist_urls"
    ALLOWLIST_EXCEPTION = "allowlist_exception_urls"
