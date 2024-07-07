from loguru import logger
from qfluentwidgets import ScrollArea, SettingCardGroup, RangeSettingCard, FluentIcon
from PySide6.QtWidgets import QWidget, QApplication
from ui_py.ui_settings_view import Ui_SettingsView

from models.config import app_settings
from config_values import ConfigValues


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

    def initLayout(self):
        self.pomodoro_settings_group.addSettingCard(self.work_duration_card)
        self.pomodoro_settings_group.addSettingCard(self.break_duration_card)
        self.pomodoro_settings_group.addSettingCard(self.long_break_duration_card)


        self.scrollAreaWidgetContents.layout().addWidget(self.pomodoro_settings_group)

    def onValueChanged(self):
        app_settings.work_duration.valueChanged.connect(self.updateWorkDuration)
        app_settings.break_duration.valueChanged.connect(self.updateBreakDuration)
        app_settings.long_break_duration.valueChanged.connect(self.updateLongBreakDuration)

    def updateBreakDuration(self):
        ConfigValues.BREAK_DURATION = app_settings.get(app_settings.break_duration)
        logger.debug(f"Break Duration: {app_settings.get(app_settings.break_duration)}")

    def updateWorkDuration(self):
        ConfigValues.WORK_DURATION = app_settings.get(app_settings.work_duration)
        logger.debug(f"Work Duration: {app_settings.get(app_settings.work_duration)}")

    def updateLongBreakDuration(self):
        ConfigValues.LONG_BREAK_DURATION = app_settings.get(app_settings.long_break_duration)
        logger.debug(f"Long Break Duration: {app_settings.get(app_settings.long_break_duration)}")


if __name__ == "__main__":
    app = QApplication()
    w = SettingsView()
    w.show()
    app.exec()
