from PySide6.QtWidgets import QWidget, QApplication
from loguru import logger
from qfluentwidgets import SettingCardGroup, RangeSettingCard, FluentIcon, SwitchSettingCard, OptionsSettingCard, \
    CustomColorSettingCard, ColorSettingCard

from config_values import ConfigValues
from models.config import workspace_specific_settings, app_settings
from prefabs.setting_cards.SpinBoxSettingCardSQL import SpinBoxSettingCardSQL
from prefabs.setting_cards.RangeSettingCardSQL import RangeSettingCardSQL
from prefabs.setting_cards.SwitchSettingCardSQL import SwitchSettingCardSQL
from qfluentwidgets import setTheme, setThemeColor
from ui_py.ui_settings_view import Ui_SettingsView


class SettingsView(QWidget, Ui_SettingsView):
    """
    For settings view of the app
    """
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
        self.work_duration_card = RangeSettingCardSQL(
            workspace_specific_settings.work_duration,
            FluentIcon.VPN,
            "Work Duration",
            "Set the work duration in minutes",
            self.pomodoro_settings_group
        )
        self.break_duration_card = RangeSettingCardSQL(
            workspace_specific_settings.break_duration,
            FluentIcon.VPN,
            "Break Duration",
            "Set the break duration in minutes",
            self.pomodoro_settings_group
        )
        self.long_break_duration_card = RangeSettingCardSQL(
            workspace_specific_settings.long_break_duration,
            FluentIcon.VPN,
            "Long Break Duration",
            "Set the long break duration in minutes",
            self.pomodoro_settings_group
        )
        self.work_interval_card = SpinBoxSettingCardSQL(
            workspace_specific_settings.work_intervals,
            FluentIcon.VPN,
            "Work Intervals",
            "Set the number of work intervals before a long break",
            self.pomodoro_settings_group
        )
        self.autostart_work_card = SwitchSettingCardSQL(
            FluentIcon.VPN,
            "Autostart Work",
            "Start work session automatically after break ends",
            workspace_specific_settings.autostart_work,
            self.pomodoro_settings_group
        )
        self.autostart_break_card = SwitchSettingCardSQL(
            FluentIcon.VPN,
            "Autostart Break",
            "Start break session automatically after work ends",
            workspace_specific_settings.autostart_break,
            self.pomodoro_settings_group
        )

        # Personalization Settings
        self.personalization_settings_group = SettingCardGroup(
            self.tr('Personalization'), self.scrollArea)
        self.theme_card = OptionsSettingCard(
            app_settings.themeMode,
            FluentIcon.BRUSH,
            self.tr('Application theme'),
            self.tr("Change the appearance of your application"),
            texts=[
                self.tr('Light'), self.tr('Dark'),
                self.tr('Use system setting')
            ],
            parent=self.personalization_settings_group
        )
        self.theme_color_card = CustomColorSettingCard(
            app_settings.themeColor,
            FluentIcon.PALETTE,
            self.tr('Theme color'),
            self.tr('Change the theme color of you application'),
            self.personalization_settings_group
        )

        self.__connectSignalToSlot()

    def initLayout(self):
        self.pomodoro_settings_group.addSettingCard(self.work_duration_card)
        self.pomodoro_settings_group.addSettingCard(self.break_duration_card)
        self.pomodoro_settings_group.addSettingCard(self.long_break_duration_card)
        self.pomodoro_settings_group.addSettingCard(self.work_interval_card)
        self.pomodoro_settings_group.addSettingCard(self.autostart_work_card)
        self.pomodoro_settings_group.addSettingCard(self.autostart_break_card)

        self.scrollAreaWidgetContents.layout().addWidget(self.pomodoro_settings_group)

        self.personalization_settings_group.addSettingCard(self.theme_card)
        self.personalization_settings_group.addSettingCard(self.theme_color_card)

        self.scrollAreaWidgetContents.layout().addWidget(self.personalization_settings_group)

    def onValueChanged(self):
        workspace_specific_settings.work_duration.valueChanged.connect(self.updateWorkDuration)
        workspace_specific_settings.break_duration.valueChanged.connect(self.updateBreakDuration)
        workspace_specific_settings.long_break_duration.valueChanged.connect(self.updateLongBreakDuration)
        workspace_specific_settings.work_intervals.valueChanged.connect(self.updateWorkIntervals)
        workspace_specific_settings.autostart_work.valueChanged.connect(self.updateAutostartWork)
        workspace_specific_settings.autostart_break.valueChanged.connect(self.updateAutostartBreak)


    def updateBreakDuration(self):
        ConfigValues.BREAK_DURATION = workspace_specific_settings.get(workspace_specific_settings.break_duration)
        logger.debug(f"Break Duration: {workspace_specific_settings.get(workspace_specific_settings.break_duration)}")

    def updateWorkDuration(self):
        ConfigValues.WORK_DURATION = workspace_specific_settings.get(workspace_specific_settings.work_duration)
        logger.debug(f"Work Duration: {workspace_specific_settings.get(workspace_specific_settings.work_duration)}")

    def updateLongBreakDuration(self):
        ConfigValues.LONG_BREAK_DURATION = workspace_specific_settings.get(workspace_specific_settings.long_break_duration)
        logger.debug(f"Long Break Duration: {workspace_specific_settings.get(workspace_specific_settings.long_break_duration)}")

    def updateWorkIntervals(self):
        ConfigValues.WORK_INTERVALS = workspace_specific_settings.get(workspace_specific_settings.work_intervals)
        logger.debug(f"Work Intervals: {workspace_specific_settings.get(workspace_specific_settings.work_intervals)}")

    def updateAutostartWork(self):
        ConfigValues.AUTOSTART_WORK = workspace_specific_settings.get(workspace_specific_settings.autostart_work)
        logger.debug(f"Autostart Work: {workspace_specific_settings.get(workspace_specific_settings.autostart_work)}")

    def updateAutostartBreak(self):
        ConfigValues.AUTOSTART_BREAK = workspace_specific_settings.get(workspace_specific_settings.autostart_break)
        logger.debug(f"Autostart Break: {workspace_specific_settings.get(workspace_specific_settings.autostart_break)}")

    def __connectSignalToSlot(self):
        self.theme_card.optionChanged.connect(lambda ci: setTheme(workspace_specific_settings.get(ci)))
        self.theme_color_card.colorChanged.connect(lambda c: setThemeColor(c))

if __name__ == "__main__":
    app = QApplication()
    w = SettingsView()
    w.show()
    app.exec()
