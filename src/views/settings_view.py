from PySide6.QtWidgets import QWidget, QApplication
from loguru import logger
from qfluentwidgets import SettingCardGroup, RangeSettingCard, FluentIcon, SwitchSettingCard

from config_values import ConfigValues
from models.config import app_settings
from prefabs.SpinBoxSettingCard import SpinBoxSettingCard
from ui_py.ui_settings_view import Ui_SettingsView


class SettingsView(QWidget, Ui_SettingsView):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.initSettings()
        self.initLayout()
        self.onValueChanged()

    def initSettings(self):
        # Pomodoro Settings
        self.pomodoro_settings_group = SettingCardGroup(
            "Pomodoro", self.scrollArea
        )
        self.work_duration_card = RangeSettingCard(
            app_settings.work_duration,
            FluentIcon.VPN,
            "Work Duration",
            "Set the work duration in minutes",
            self.pomodoro_settings_group
        )
        self.break_duration_card = RangeSettingCard(
            app_settings.break_duration,
            FluentIcon.VPN,
            "Break Duration",
            "Set the break duration in minutes",
            self.pomodoro_settings_group
        )
        self.long_break_duration_card = RangeSettingCard(
            app_settings.long_break_duration,
            FluentIcon.VPN,
            "Long Break Duration",
            "Set the long break duration in minutes",
            self.pomodoro_settings_group
        )
        self.work_interval_card = SpinBoxSettingCard(
            app_settings.work_intervals,
            FluentIcon.VPN,
            "Work Intervals",
            "Set the number of work intervals before a long break",
            self.pomodoro_settings_group
        )
        self.autostart_work_card = SwitchSettingCard(
            FluentIcon.VPN,
            "Autostart Work",
            "Start work session automatically after break ends",
            app_settings.autostart_work,
            self.pomodoro_settings_group
        )
        self.autostart_break_card = SwitchSettingCard(
            FluentIcon.VPN,
            "Autostart Break",
            "Start break session automatically after work ends",
            app_settings.autostart_break,
            self.pomodoro_settings_group
        )

    def initLayout(self):
        self.pomodoro_settings_group.addSettingCard(self.work_duration_card)
        self.pomodoro_settings_group.addSettingCard(self.break_duration_card)
        self.pomodoro_settings_group.addSettingCard(self.long_break_duration_card)
        self.pomodoro_settings_group.addSettingCard(self.work_interval_card)
        self.pomodoro_settings_group.addSettingCard(self.autostart_work_card)
        self.pomodoro_settings_group.addSettingCard(self.autostart_break_card)

        self.scrollAreaWidgetContents.layout().addWidget(self.pomodoro_settings_group)

    def onValueChanged(self):
        app_settings.work_duration.valueChanged.connect(self.updateWorkDuration)
        app_settings.break_duration.valueChanged.connect(self.updateBreakDuration)
        app_settings.long_break_duration.valueChanged.connect(self.updateLongBreakDuration)
        app_settings.work_intervals.valueChanged.connect(self.updateWorkIntervals)
        app_settings.autostart_work.valueChanged.connect(self.updateAutostartWork)
        app_settings.autostart_break.valueChanged.connect(self.updateAutostartBreak)


    def updateBreakDuration(self):
        ConfigValues.BREAK_DURATION = app_settings.get(app_settings.break_duration)
        logger.debug(f"Break Duration: {app_settings.get(app_settings.break_duration)}")

    def updateWorkDuration(self):
        ConfigValues.WORK_DURATION = app_settings.get(app_settings.work_duration)
        logger.debug(f"Work Duration: {app_settings.get(app_settings.work_duration)}")

    def updateLongBreakDuration(self):
        ConfigValues.LONG_BREAK_DURATION = app_settings.get(app_settings.long_break_duration)
        logger.debug(f"Long Break Duration: {app_settings.get(app_settings.long_break_duration)}")

    def updateWorkIntervals(self):
        ConfigValues.WORK_INTERVALS = app_settings.get(app_settings.work_intervals)
        logger.debug(f"Work Intervals: {app_settings.get(app_settings.work_intervals)}")

    def updateAutostartWork(self):
        ConfigValues.AUTOSTART_WORK = app_settings.get(app_settings.autostart_work)
        logger.debug(f"Autostart Work: {app_settings.get(app_settings.autostart_work)}")

    def updateAutostartBreak(self):
        ConfigValues.AUTOSTART_BREAK = app_settings.get(app_settings.autostart_break)
        logger.debug(f"Autostart Break: {app_settings.get(app_settings.autostart_break)}")


if __name__ == "__main__":
    app = QApplication()
    w = SettingsView()
    w.show()
    app.exec()
