import os

from PySide6.QtCore import QSettings, QCoreApplication
from qfluentwidgets import QConfig, qconfig, RangeConfigItem, RangeValidator, ConfigItem, BoolValidator, Theme

from constants import ORGANIZATION_NAME, APPLICATION_NAME


class Settings(QConfig):
    """
    Used for storing settings of the app.
    Documentation for QConfig is here: https://qfluentwidgets.com/pages/components/config/#usage
    """

    work_duration = RangeConfigItem("Pomodoro", "WorkDuration", 25, RangeValidator(1, 240))
    break_duration = RangeConfigItem("Pomodoro", "BreakDuration", 5, RangeValidator(1, 60))
    long_break_duration = RangeConfigItem("Pomodoro", "LongBreakDuration", 15,
                                          RangeValidator(1, 60))
    work_intervals = RangeConfigItem("Pomodoro", "WorkIntervals", 2, RangeValidator(1, 4))
    autostart_work = ConfigItem("Pomodoro", "AutostartWork", True, BoolValidator())
    autostart_break = ConfigItem("Pomodoro", "AutostartBreak", True, BoolValidator())


QCoreApplication.setOrganizationName(ORGANIZATION_NAME)
QCoreApplication.setApplicationName(APPLICATION_NAME)

# will be used for saving settings
app_settings = Settings()

# will only be used to get platform specific file save location, all config values are to be saved using qconfig
setting_temp = QSettings(QSettings.Format.IniFormat, QSettings.Scope.UserScope, ORGANIZATION_NAME, APPLICATION_NAME)

settings_dir = os.path.dirname(setting_temp.fileName())

# replacing the extension of the settings file from .ini to .json
root, _ = os.path.splitext(setting_temp.fileName())
settings_file_path = root + ".json"

db_path = os.path.join(settings_dir, f"{APPLICATION_NAME}.db")

app_settings.themeMode.value = Theme.AUTO
qconfig.load(settings_file_path, app_settings)
