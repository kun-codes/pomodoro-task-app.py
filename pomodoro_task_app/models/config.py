from qfluentwidgets import BoolValidator, ConfigItem, QConfig, RangeConfigItem, RangeValidator, Theme, qconfig

from config_paths import settings_file_path
from constants import (
    AUTOSTART_BREAK,
    AUTOSTART_WORK,
    BREAK_DURATION,
    ENABLE_WEBSITE_FILTER,
    LONG_BREAK_DURATION,
    WORK_DURATION,
    WORK_INTERVALS,
)
from models.db_tables import Workspace
from prefabs.config.config_item_sql import ConfigItemSQL, RangeConfigItemSQL
from prefabs.config.qconfig_sql import QConfigSQL, qconfig_custom
from utils.is_win_11 import isWin11


class WorkspaceSettings(QConfigSQL):
    """
    Used for storing settings unique to a workspace in the app.
    Documentation for QConfig is here: https://qfluentwidgets.com/pages/components/config/#usage
    """

    work_duration = RangeConfigItemSQL(Workspace, Workspace.work_duration, WORK_DURATION, RangeValidator(1, 240))
    break_duration = RangeConfigItemSQL(Workspace, Workspace.break_duration, BREAK_DURATION, RangeValidator(1, 60))
    long_break_duration = RangeConfigItemSQL(
        Workspace, Workspace.long_break_duration, LONG_BREAK_DURATION, RangeValidator(1, 60)
    )
    work_intervals = RangeConfigItemSQL(Workspace, Workspace.work_intervals, WORK_INTERVALS, RangeValidator(1, 10))
    autostart_work = ConfigItemSQL(Workspace, Workspace.autostart_work, AUTOSTART_WORK, BoolValidator())
    autostart_break = ConfigItemSQL(Workspace, Workspace.autostart_break, AUTOSTART_BREAK, BoolValidator())
    enable_website_filter = ConfigItemSQL(
        Workspace, Workspace.enable_website_filter, ENABLE_WEBSITE_FILTER, BoolValidator()
    )


class AppSettings(QConfig):
    """
    Used for storing settings that are not workspace specific and global to the app.
    Documentation for QConfig is here: https://qfluentwidgets.com/pages/components/config/#usage
    """

    proxy_port = RangeConfigItem("AppSettings", "ProxyPort", 8080, RangeValidator(1024, 65535))
    check_for_updates_on_start = ConfigItem("AppSettings", "CheckForUpdatesOnStart", True, BoolValidator())
    has_visited_task_view = ConfigItem("AppSettings", "HasVisitedTaskView", False, BoolValidator())
    has_visited_pomodoro_view = ConfigItem("AppSettings", "HasVisitedPomodoroView", False, BoolValidator())
    has_visited_website_filter_view = ConfigItem("AppSettings", "HasVisitedWebsiteFilterView", False, BoolValidator())
    mica_enabled = ConfigItem("MainWindow", "MicaEnabled", isWin11(), BoolValidator())


workspace_specific_settings = WorkspaceSettings()
app_settings = AppSettings()

app_settings.themeMode.value = Theme.AUTO


def load_workspace_settings():
    qconfig_custom.load("", workspace_specific_settings)  # passing empty string as the path as function asks for path
    # to json file which stores settings and we are using db to store settings


def load_app_settings():
    qconfig.load(settings_file_path, app_settings)


load_app_settings()
load_workspace_settings()
