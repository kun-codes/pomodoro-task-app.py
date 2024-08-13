from qfluentwidgets import RangeValidator, BoolValidator, Theme, qconfig, QConfig
from prefabs.config.qconfig_sql import qconfig_custom

from constants import WORK_DURATION, BREAK_DURATION, LONG_BREAK_DURATION, WORK_INTERVALS, AUTOSTART_WORK, \
    AUTOSTART_BREAK
from config_paths import settings_file_path
from prefabs.config.config_item_sql import RangeConfigItemSQL, ConfigItemSQL
from models.db_tables import Workspace
from prefabs.config.qconfig_sql import QConfigSQL


class WorkspaceSettings(QConfigSQL):
    """
    Used for storing settings unique to a workspace in the app.
    Documentation for QConfig is here: https://qfluentwidgets.com/pages/components/config/#usage
    """

    work_duration = RangeConfigItemSQL(Workspace, Workspace.work_duration, WORK_DURATION, RangeValidator(1, 240))
    break_duration = RangeConfigItemSQL(Workspace, Workspace.break_duration, BREAK_DURATION, RangeValidator(1, 60))
    long_break_duration = RangeConfigItemSQL(Workspace, Workspace.long_break_duration, LONG_BREAK_DURATION,
                                             RangeValidator(1, 60))
    work_intervals = RangeConfigItemSQL(Workspace, Workspace.work_intervals, WORK_INTERVALS, RangeValidator(1, 10))
    autostart_work = ConfigItemSQL(Workspace, Workspace.autostart_work, AUTOSTART_WORK, BoolValidator())
    autostart_break = ConfigItemSQL(Workspace, Workspace.autostart_break, AUTOSTART_BREAK, BoolValidator())


class AppSettings(QConfig):
    """
    Used for storing settings that are not workspace specific and global to the app.
    Documentation for QConfig is here: https://qfluentwidgets.com/pages/components/config/#usage
    """
    pass


workspace_specific_settings = WorkspaceSettings()
app_settings = AppSettings()

app_settings.themeMode.value = Theme.AUTO
def load_workspace_settings():
    qconfig_custom.load("", workspace_specific_settings)  # passing empty string as the path as function asks for path
    # to json file which stores settings and we are using db to store settings
def load_app_settings():
    qconfig.load(settings_file_path,app_settings)

load_app_settings()
load_workspace_settings()
