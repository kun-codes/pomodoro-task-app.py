from config_values import ConfigValues
from loguru import logger
from models.config import app_settings, workspace_specific_settings
from prefabs.customFluentIcon import CustomFluentIcon
from prefabs.setting_cards.RangeSettingCardSQL import RangeSettingCardSQL
from prefabs.setting_cards.SpinBoxSettingCard import SpinBoxSettingCard
from prefabs.setting_cards.SpinBoxSettingCardSQL import SpinBoxSettingCardSQL
from prefabs.setting_cards.SwitchSettingCardSQL import SwitchSettingCardSQL
from PySide6.QtWidgets import QApplication, QWidget
from qfluentwidgets import (
    CustomColorSettingCard,
    FluentIcon,
    OptionsSettingCard,
    SettingCardGroup,
    SwitchSettingCard,
    setTheme,
    setThemeColor,
)
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
        # self.initQss()
        self.onValueChanged()

    def initSettings(self):
        # Pomodoro Settings
        self.pomodoro_settings_group = SettingCardGroup("Pomodoro", self.scrollArea)
        self.work_duration_card = RangeSettingCardSQL(
            workspace_specific_settings.work_duration,
            CustomFluentIcon.WORK,
            "Work Duration",
            "Set the work duration in minutes",
            self.pomodoro_settings_group,
        )
        self.break_duration_card = RangeSettingCardSQL(
            workspace_specific_settings.break_duration,
            CustomFluentIcon.BREAK,
            "Break Duration",
            "Set the break duration in minutes",
            self.pomodoro_settings_group,
        )
        self.long_break_duration_card = RangeSettingCardSQL(
            workspace_specific_settings.long_break_duration,
            CustomFluentIcon.LONG_BREAK,
            "Long Break Duration",
            "Set the long break duration in minutes",
            self.pomodoro_settings_group,
        )
        self.work_interval_card = SpinBoxSettingCardSQL(
            workspace_specific_settings.work_intervals,
            CustomFluentIcon.WORK_INTERVAL,
            "Work Intervals",
            "Set the number of work intervals before a long break",
            self.pomodoro_settings_group,
        )
        self.autostart_work_card = SwitchSettingCardSQL(
            CustomFluentIcon.AUTOSTART_WORK,
            "Autostart Work",
            "Start work session automatically after break ends",
            workspace_specific_settings.autostart_work,
            self.pomodoro_settings_group,
        )
        self.autostart_break_card = SwitchSettingCardSQL(
            CustomFluentIcon.AUTOSTART_BREAK,
            "Autostart Break",
            "Start break session automatically after work ends",
            workspace_specific_settings.autostart_break,
            self.pomodoro_settings_group,
        )

        # Website Filter Settings
        self.website_filter_settings_group = SettingCardGroup("Website Filter", self.scrollArea)
        self.enable_website_filter_card = SwitchSettingCardSQL(
            CustomFluentIcon.WEBSITE_FILTER_VIEW,
            "Enable Website Filter",
            "Enable website filtering",
            workspace_specific_settings.enable_website_filter,
            self.website_filter_settings_group,
        )
        self.proxy_port_card = SpinBoxSettingCard(
            app_settings.proxy_port,
            CustomFluentIcon.PORT,
            "Proxy Port",
            "Select the port where the website filter runs",
            self.website_filter_settings_group,
        )

        # Personalization Settings
        self.personalization_settings_group = SettingCardGroup(self.tr("Personalization"), self.scrollArea)
        self.theme_card = OptionsSettingCard(
            app_settings.themeMode,
            FluentIcon.BRUSH,
            self.tr("Application theme"),
            self.tr("Change the appearance of your application"),
            texts=[self.tr("Light"), self.tr("Dark"), self.tr("Use system setting")],
            parent=self.personalization_settings_group,
        )
        self.theme_color_card = CustomColorSettingCard(
            app_settings.themeColor,
            FluentIcon.PALETTE,
            self.tr("Theme color"),
            self.tr("Change the theme color of you application"),
            self.personalization_settings_group,
        )

        # Update Settings
        self.update_settings_group = SettingCardGroup("Updates", self.scrollArea)
        self.check_for_updates_on_start_card = SwitchSettingCard(
            FluentIcon.UPDATE,
            "Check For Updates On Start",
            "The new version will be more stable and have more features",
            app_settings.check_for_updates_on_start,
            self.update_settings_group,
        )

        self.__connectSignalToSlot()

    def initLayout(self):
        self.pomodoro_settings_group.addSettingCard(self.work_duration_card)
        self.pomodoro_settings_group.addSettingCard(self.break_duration_card)
        self.pomodoro_settings_group.addSettingCard(self.long_break_duration_card)
        self.pomodoro_settings_group.addSettingCard(self.work_interval_card)
        self.pomodoro_settings_group.addSettingCard(self.autostart_work_card)
        self.pomodoro_settings_group.addSettingCard(self.autostart_break_card)

        self.work_interval_card.spinBox.setMinimumWidth(125)

        self.scrollAreaWidgetContents.layout().addWidget(self.pomodoro_settings_group)

        self.website_filter_settings_group.addSettingCard(self.enable_website_filter_card)
        self.website_filter_settings_group.addSettingCard(self.proxy_port_card)

        self.proxy_port_card.spinBox.setSymbolVisible(False)
        self.proxy_port_card.spinBox.setMinimumWidth(150)

        self.scrollAreaWidgetContents.layout().addWidget(self.website_filter_settings_group)

        self.personalization_settings_group.addSettingCard(self.theme_card)
        self.personalization_settings_group.addSettingCard(self.theme_color_card)

        self.scrollAreaWidgetContents.layout().addWidget(self.personalization_settings_group)

        self.update_settings_group.addSettingCard(self.check_for_updates_on_start_card)

        self.scrollAreaWidgetContents.layout().addWidget(self.update_settings_group)

    # todo: change colour of Labels when in disabled state
    # https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/314#issuecomment-1614427404
    # def initQss(self):
    #     qss_light = """
    #     FluentLabelBase:disabled {
    #         color: lightgray;
    #     }
    #     """
    #     qss_dark = """
    #     FluentLabelBase:disabled {
    #         color: darkgray;
    #     }
    #     """
    #
    #
    #     # from: https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/707
    #     self.style().unpolish(self)
    #     self.style().polish(self)
    #
    #     setCustomStyleSheet(self, qss_light, qss_dark)
    #
    #     self.TitleLabel.setDisabled(True)
    #

    def onValueChanged(self):
        workspace_specific_settings.work_duration.valueChanged.connect(self.updateWorkDuration)
        workspace_specific_settings.break_duration.valueChanged.connect(self.updateBreakDuration)
        workspace_specific_settings.long_break_duration.valueChanged.connect(self.updateLongBreakDuration)
        workspace_specific_settings.work_intervals.valueChanged.connect(self.updateWorkIntervals)
        workspace_specific_settings.autostart_work.valueChanged.connect(self.updateAutostartWork)
        workspace_specific_settings.autostart_break.valueChanged.connect(self.updateAutostartBreak)
        workspace_specific_settings.enable_website_filter.valueChanged.connect(self.updateEnableWebsiteFilter)

        app_settings.proxy_port.valueChanged.connect(self.updateProxyPort)
        app_settings.check_for_updates_on_start.valueChanged.connect(self.updateCheckForUpdatesOnStart)

    def updateBreakDuration(self):
        ConfigValues.BREAK_DURATION = workspace_specific_settings.get(workspace_specific_settings.break_duration)
        logger.debug(f"Break Duration: {workspace_specific_settings.get(workspace_specific_settings.break_duration)}")

    def updateWorkDuration(self):
        ConfigValues.WORK_DURATION = workspace_specific_settings.get(workspace_specific_settings.work_duration)
        logger.debug(f"Work Duration: {workspace_specific_settings.get(workspace_specific_settings.work_duration)}")

    def updateLongBreakDuration(self):
        ConfigValues.LONG_BREAK_DURATION = workspace_specific_settings.get(
            workspace_specific_settings.long_break_duration
        )
        logger.debug(
            f"Long Break Duration: {workspace_specific_settings.get(workspace_specific_settings.long_break_duration)}"
        )

    def updateWorkIntervals(self):
        ConfigValues.WORK_INTERVALS = workspace_specific_settings.get(workspace_specific_settings.work_intervals)
        logger.debug(f"Work Intervals: {workspace_specific_settings.get(workspace_specific_settings.work_intervals)}")

    def updateAutostartWork(self):
        ConfigValues.AUTOSTART_WORK = workspace_specific_settings.get(workspace_specific_settings.autostart_work)
        logger.debug(f"Autostart Work: {workspace_specific_settings.get(workspace_specific_settings.autostart_work)}")

    def updateAutostartBreak(self):
        ConfigValues.AUTOSTART_BREAK = workspace_specific_settings.get(workspace_specific_settings.autostart_break)
        logger.debug(f"Autostart Break: {workspace_specific_settings.get(workspace_specific_settings.autostart_break)}")

    def updateEnableWebsiteFilter(self):
        ConfigValues.ENABLE_WEBSITE_FILTER = workspace_specific_settings.get(
            workspace_specific_settings.enable_website_filter
        )
        logger.debug(
            f"Enable Website Filter: {workspace_specific_settings.get(
                workspace_specific_settings.enable_website_filter
            )}"
        )

    def updateProxyPort(self):
        ConfigValues.PROXY_PORT = app_settings.get(app_settings.proxy_port)
        logger.debug(f"Proxy Port: {app_settings.get(app_settings.proxy_port)}")

    def updateCheckForUpdatesOnStart(self):
        ConfigValues.CHECK_FOR_UPDATES_ON_START = app_settings.get(app_settings.check_for_updates_on_start)
        logger.debug(f"Check For Updates On Start: {app_settings.get(app_settings.check_for_updates_on_start)}")

    def __connectSignalToSlot(self):
        self.theme_card.optionChanged.connect(lambda ci: setTheme(workspace_specific_settings.get(ci)))
        self.theme_color_card.colorChanged.connect(lambda c: setThemeColor(c))
        # self.proxy_port_card.valueChanged.connect


if __name__ == "__main__":
    app = QApplication()
    w = SettingsView()
    w.show()
    app.exec()
