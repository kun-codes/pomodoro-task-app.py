from qfluentwidgets import ScrollArea, SettingCardGroup, RangeSettingCard, FluentIcon
from PySide6.QtWidgets import QWidget, QApplication
from ui_py.ui_settings_view import Ui_SettingsView

from models.config import app_settings


class SettingsView(QWidget, Ui_SettingsView):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.initSettings()
        self.initLayout()

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


if __name__ == "__main__":
    app = QApplication()
    w = SettingsView()
    w.show()
    app.exec()
