import platform
from pathlib import Path

import darkdetect
from config_paths import settings_dir
from config_values import ConfigValues
from constants import FIRST_RUN_DOTFILE_NAME, TimerState, UpdateCheckResult, URLListType, WebsiteFilterType
from loguru import logger
from models.config import load_workspace_settings, workspace_specific_settings
from models.db_tables import TaskType
from models.task_list_model import TaskListModel
from models.workspace_list_model import WorkspaceListModel
from prefabs.customFluentIcon import CustomFluentIcon
from prefabs.pomodoroFluentWindow import PomodoroFluentWindow
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices, QIcon
from PySide6.QtWidgets import QMenu, QSystemTrayIcon
from qfluentwidgets import (
    FluentIcon,
    InfoBar,
    InfoBarPosition,
    MessageBox,
    NavigationItemPosition,
    SystemThemeListener,
    Theme,
)
from resources import logos_rc
from utils.check_for_updates import checkForUpdates
from utils.check_valid_db import checkValidDB
from utils.find_mitmdump_executable import get_mitmdump_path
from utils.time_conversion import convert_ms_to_hh_mm_ss
from views.dialogs.setupAppDialog import SetupAppDialog
from views.dialogs.updateDialog import UpdateDialog
from views.dialogs.workspaceManagerDialog import ManageWorkspaceDialog
from views.subinterfaces.pomodoro_view import PomodoroView
from views.subinterfaces.settings_view import SettingsView
from views.subinterfaces.tasks_view import TaskListView
from views.subinterfaces.website_blocker_view import WebsiteBlockerView
from website_blocker.website_blocker_manager import WebsiteBlockerManager


class MainWindow(PomodoroFluentWindow):
    def __init__(self):
        super().__init__()

        self.is_first_run = self.check_first_run()
        # self.checkForUpdates()
        checkValidDB()

        self.workplace_list_model = WorkspaceListModel()

        self.task_interface = TaskListView()
        self.task_interface.setObjectName("task_interface")

        self.pomodoro_interface = PomodoroView()
        self.pomodoro_interface.setObjectName("pomodoro_interface")

        self.settings_interface = SettingsView()
        self.settings_interface.setObjectName("settings_interface")

        self.website_filter_interface = WebsiteBlockerView(self.workplace_list_model)
        self.website_filter_interface.setObjectName("website_filter_interface")

        self.manage_workspace_dialog = None

        self.website_blocker_manager = WebsiteBlockerManager()

        self.themeListener = SystemThemeListener(self)
        self.themeListener.start()

        self.connectSignalsToSlots()
        self.initNavigation()
        self.initWindow()
        self.initSystemTray()
        self.initBottomBar()

        self.website_filter_interface.setEnabled(ConfigValues.ENABLE_WEBSITE_FILTER)

        self.navigationInterface.panel.setFixedHeight(48)

        self.updateDialog = None

        if self.is_first_run:
            self.setupMitmproxy()  # self.checkForUpdates() is eventually called later due to this method call
        else:
            if ConfigValues.CHECK_FOR_UPDATES_ON_START:
                self.handleUpdates()

    def initNavigation(self):
        # Add sub interface
        self.addSubInterface(self.task_interface, CustomFluentIcon.TASKS_VIEW, "Tasks")
        self.addSubInterface(self.pomodoro_interface, FluentIcon.STOP_WATCH, "Pomodoro")
        self.addSubInterface(self.website_filter_interface, CustomFluentIcon.WEBSITE_FILTER_VIEW, "Website Filter")

        # Add sub interface at bottom
        self.navigationInterface.addItem(
            routeKey="WorkspaceSelector",
            icon=CustomFluentIcon.WORKSPACE_SELECTOR_VIEW,
            text="Select Workspace",
            onClick=lambda: self.onWorkspaceManagerClicked(),
            selectable=False,
            tooltip="Select the workspace to work in",
            position=NavigationItemPosition.BOTTOM,
        )
        self.addSubInterface(self.settings_interface, FluentIcon.SETTING, "Settings", NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(1000, 800)
        self.setMinimumWidth(715)
        self.setWindowTitle("Pomodoro Task List App")
        self.setWindowIcon(QIcon(":/logosPrefix/logos/logo.svg"))

    def initSystemTray(self):
        """Initialize system tray icon and notifications"""
        self.tray = QSystemTrayIcon(self)

        self.tray_menu = QMenu()

        is_os_dark_mode = darkdetect.isDark()

        self.tray_menu_timer_status_action = self.tray_menu.addAction("Timer not running")
        self.tray_menu_timer_status_action.setIcon(
            FluentIcon.STOP_WATCH.icon(Theme.DARK if is_os_dark_mode else Theme.LIGHT)
        )
        self.tray_menu_timer_status_action.setEnabled(False)  # Make it non-clickable

        self.tray_menu.addSeparator()

        # Timer control actions
        # context menu of Windows system tray icon is always in light mode for qt apps. Tested on Windows 10, didn't
        # test on Windows 11 yet
        self.tray_menu_start_action = self.tray_menu.addAction("Start")
        self.tray_menu_start_action.setIcon(
            FluentIcon.PLAY.icon(Theme.DARK if is_os_dark_mode and not platform.system() == "Windows" else Theme.LIGHT)
        )
        self.tray_menu_start_action.triggered.connect(lambda: self.pomodoro_interface.pauseResumeButton.click())

        self.tray_menu_pause_resume_action = self.tray_menu.addAction("Pause/Resume")
        self.tray_menu_pause_resume_action.setIcon(
            CustomFluentIcon.PLAY_PAUSE.icon(
                Theme.DARK if is_os_dark_mode and not platform.system() == "Windows" else Theme.LIGHT
            )
        )
        self.tray_menu_pause_resume_action.triggered.connect(lambda: self.pomodoro_interface.pauseResumeButton.click())
        self.tray_menu_pause_resume_action.setEnabled(False)

        self.tray_menu_stop_action = self.tray_menu.addAction("Stop")
        self.tray_menu_stop_action.setIcon(
            FluentIcon.CLOSE.icon(Theme.DARK if is_os_dark_mode and not platform.system() == "Windows" else Theme.LIGHT)
        )
        self.tray_menu_stop_action.triggered.connect(lambda: self.pomodoro_interface.stopButton.click())

        self.tray_menu_skip_action = self.tray_menu.addAction("Skip")
        self.tray_menu_skip_action.setIcon(
            FluentIcon.CHEVRON_RIGHT.icon(
                Theme.DARK if is_os_dark_mode and not platform.system() == "Windows" else Theme.LIGHT
            )
        )
        self.tray_menu_skip_action.triggered.connect(lambda: self.pomodoro_interface.skipButton.click())

        self.tray_menu.addSeparator()

        self.tray_menu_quit_action = self.tray_menu.addAction("Quit")
        self.tray_menu_quit_action.setIcon(
            CustomFluentIcon.EXIT.icon(
                Theme.DARK if is_os_dark_mode and not platform.system() == "Windows" else Theme.LIGHT
            )
        )
        self.tray_menu_quit_action.triggered.connect(self.close)

        self.tray.setContextMenu(self.tray_menu)

        self.tray_white_icon = QIcon(":/logosPrefix/logos/logo-monochrome-white.svg")
        self.tray_black_icon = QIcon(":/logosPrefix/logos/logo-monochrome-black.svg")

        if is_os_dark_mode:
            initial_icon = self.tray_white_icon
        else:
            initial_icon = self.tray_black_icon

        self.tray.setIcon(initial_icon)
        self.tray.setVisible(True)

    def updateSystemTrayIcon(self):
        logger.debug("Updating system tray icon")
        # context menu of Windows system tray icon is always in light mode for qt apps. Tested on Windows 10, didn't
        # test on Windows 11 yet
        if darkdetect.isDark():
            self.tray.setIcon(self.tray_white_icon)
        else:
            self.tray.setIcon(self.tray_black_icon)

        if platform.system() == "Windows":
            return

        if darkdetect.isDark():
            self.tray_menu_timer_status_action.setIcon(FluentIcon.STOP_WATCH.icon(Theme.DARK))
            self.tray_menu_start_action.setIcon(FluentIcon.PLAY.icon(Theme.DARK))
            self.tray_menu_pause_resume_action.setIcon(CustomFluentIcon.PLAY_PAUSE.icon(Theme.DARK))
            self.tray_menu_stop_action.setIcon(FluentIcon.CLOSE.icon(Theme.DARK))
            self.tray_menu_skip_action.setIcon(FluentIcon.CHEVRON_RIGHT.icon(Theme.DARK))
            self.tray_menu_quit_action.setIcon(CustomFluentIcon.EXIT.icon(Theme.DARK))
        else:
            self.tray_menu_timer_status_action.setIcon(FluentIcon.STOP_WATCH.icon(Theme.LIGHT))
            self.tray_menu_start_action.setIcon(FluentIcon.PLAY.icon(Theme.LIGHT))
            self.tray_menu_pause_resume_action.setIcon(CustomFluentIcon.PLAY_PAUSE.icon(Theme.LIGHT))
            self.tray_menu_stop_action.setIcon(FluentIcon.CLOSE.icon(Theme.LIGHT))
            self.tray_menu_skip_action.setIcon(FluentIcon.CHEVRON_RIGHT.icon(Theme.LIGHT))
            self.tray_menu_quit_action.setIcon(CustomFluentIcon.EXIT.icon(Theme.LIGHT))

    def updateSystemTrayActions(self, timerState):
        if timerState in [TimerState.WORK, TimerState.BREAK, TimerState.LONG_BREAK]:
            self.tray_menu_pause_resume_action.setEnabled(True)
            self.tray_menu_start_action.setEnabled(False)
        else:
            self.tray_menu_pause_resume_action.setEnabled(False)
            self.tray_menu_start_action.setEnabled(True)

    # below 4 methods are for the bottom bar
    def initBottomBar(self):
        self.update_bottom_bar_timer_label()

        self.bottomBar.pauseResumeButton.setCheckable(True)
        self.bottomBar.pauseResumeButton.setChecked(True)
        self.bottomBar.pauseResumeButton.setIcon(FluentIcon.PLAY)
        self.bottomBar.pauseResumeButton.clicked.connect(self.bottomBarPauseResumeButtonClicked)
        self.bottomBar.skipButton.clicked.connect(self.pomodoro_interface.skipButtonClicked)
        self.bottomBar.stopButton.clicked.connect(self.pomodoro_interface.stopButtonClicked)

        self.bottomBar.taskLabel.setText("Current Task: None")

    def bottomBarPauseResumeButtonClicked(self):
        # Sync state with pomodoro view button
        self.pomodoro_interface.pauseResumeButton.setChecked(self.bottomBar.pauseResumeButton.isChecked())
        self.pomodoro_interface.pauseResumeButtonClicked()

        # Update bottom bar button icon
        if self.bottomBar.pauseResumeButton.isChecked():
            self.bottomBar.pauseResumeButton.setIcon(FluentIcon.PLAY)
        else:
            self.bottomBar.pauseResumeButton.setIcon(FluentIcon.PAUSE)

    def syncBottomBarPauseResumeButton(self):
        """Sync bottom bar button state with pomodoro view button"""
        self.bottomBar.pauseResumeButton.setChecked(self.pomodoro_interface.pauseResumeButton.isChecked())
        if self.bottomBar.pauseResumeButton.isChecked():
            self.bottomBar.pauseResumeButton.setIcon(FluentIcon.PLAY)
        else:
            self.bottomBar.pauseResumeButton.setIcon(FluentIcon.PAUSE)

    def changeBottomBarPauseResumeButtonCheckedState(self, checked_state: bool):
        """Reset bottom bar button to initial state"""
        if checked_state:
            self.bottomBar.pauseResumeButton.setChecked(True)
            self.bottomBar.pauseResumeButton.setIcon(FluentIcon.PLAY)
        else:
            self.bottomBar.pauseResumeButton.setIcon(FluentIcon.PAUSE)
            self.bottomBar.pauseResumeButton.setChecked(False)

    def showNotifications(self, timerState, isSkipped):
        title = ""
        message = ""

        work_duration = ConfigValues.WORK_DURATION
        break_duration = ConfigValues.BREAK_DURATION
        long_break_duration = ConfigValues.LONG_BREAK_DURATION

        if timerState == TimerState.WORK:
            if ConfigValues.AUTOSTART_WORK or (not ConfigValues.AUTOSTART_WORK and isSkipped):
                # if ConfigValues.AUTOSTART_WORK:
                title = "Work Session Started"
                message = f"{work_duration}m work session has started"
            elif not ConfigValues.AUTOSTART_WORK and not self.pomodoro_interface.isInitialWorkSession():
                # no point in showing that break has ended when work session is for the first time
                if self.pomodoro_interface.pomodoro_timer_obj.getSessionProgress() == 0.5:  # long break ended
                    title = "Long Break Ended"
                    message = "Long break has ended. Start the next work session"
                else:  # break ended
                    title = "Break Ended"
                    message = "Break has ended. Start the next work session"
        elif timerState in [TimerState.BREAK, TimerState.LONG_BREAK]:
            if ConfigValues.AUTOSTART_BREAK or (not ConfigValues.AUTOSTART_BREAK and isSkipped):
                if self.pomodoro_interface.pomodoro_timer_obj.getSessionProgress() == ConfigValues.WORK_INTERVALS:
                    title = "Long Break Session Started"
                    message = f"{long_break_duration}m long break session has started"
                else:
                    title = "Break Session Started"
                    message = f"{break_duration}m break session has started"
            else:
                if self.pomodoro_interface.pomodoro_timer_obj.getSessionProgress() == ConfigValues.WORK_INTERVALS:
                    title = "Work Session Ended"
                    message = "Work session has ended. Start the next long break session"
                else:
                    title = "Work Session Ended"
                    message = "Work session has ended. Start the next break session"
        elif timerState == TimerState.NOTHING:
            title = "Timer Stopped"
            message = "Timer has stopped"

        if title and message:
            self.tray.showMessage(
                title,
                message,
                QSystemTrayIcon.Information,
                5000,
            )

    def onWorkspaceManagerClicked(self):
        if self.manage_workspace_dialog is None:
            self.manage_workspace_dialog = ManageWorkspaceDialog(
                parent=self.window(), workspaceListModel=self.workplace_list_model
            )

        self.manage_workspace_dialog.show()

    def toggleUIElementsBasedOnTimerState(self, timerState):
        logger.warning(f"timerState: {timerState}")
        logger.warning("timerStateChangedSignal emited")
        logger.warning(
            f"Time left in current duration: {self.pomodoro_interface.pomodoro_timer_obj.getRemainingTime()}"
        )
        # TODO: show a tip to stop the timer before changing settings when timer is running
        workspace_selector_button = self.navigationInterface.panel.widget("WorkspaceSelector")
        if timerState in [TimerState.WORK, TimerState.BREAK, TimerState.LONG_BREAK]:
            self.settings_interface.pomodoro_settings_group.setDisabled(True)
            workspace_selector_button.setDisabled(True)
            self.settings_interface.proxy_port_card.setDisabled(True)
        else:
            self.settings_interface.pomodoro_settings_group.setDisabled(False)
            workspace_selector_button.setDisabled(False)
            self.settings_interface.proxy_port_card.setDisabled(False)

    def toggle_website_filtering(self, timerState):
        if not ConfigValues.ENABLE_WEBSITE_FILTER:
            logger.debug("Website filtering is disabled, so not starting website filtering")
            self.website_blocker_manager.stop_filtering(delete_proxy=True)
            return

        logger.debug("Website filtering is enabled, so starting website filtering")
        website_filter_type = self.website_filter_interface.model.get_website_filter_type()
        logger.debug(f"website_filter_type: {website_filter_type}")

        urls = None
        block_type = None

        if website_filter_type == WebsiteFilterType.BLOCKLIST:  # blocklist
            urls = self.website_filter_interface.model.get_urls(URLListType.BLOCKLIST)
            block_type = "blocklist"
        elif website_filter_type == WebsiteFilterType.ALLOWLIST:  # allowlist
            urls = self.website_filter_interface.model.get_urls(URLListType.ALLOWLIST)
            block_type = "allowlist"

        logger.debug(f"URLs: {urls}")
        logger.debug(f"Block type: {block_type}")

        if urls is not None:  # find what to do when there are no urls registered
            joined_urls = ",".join(urls)

        mitmdump_path = get_mitmdump_path()

        if timerState == TimerState.WORK:
            # todo: check if the timer is running before starting the website filtering, because in case autostart work
            #   is off, the website filter would start even when the timer is not running
            logger.debug("Starting website filtering")
            self.website_blocker_manager.start_filtering(
                ConfigValues.PROXY_PORT, joined_urls, block_type, mitmdump_path
            )
        else:
            logger.debug("Stopping website filtering")
            self.website_blocker_manager.stop_filtering(delete_proxy=True)

    def is_task_beginning(self):
        current_state = self.pomodoro_interface.pomodoro_timer_obj.getTimerState()
        previous_state = self.pomodoro_interface.pomodoro_timer_obj.previous_timer_state

        return (
            previous_state in [TimerState.NOTHING, TimerState.BREAK, TimerState.LONG_BREAK]
            and current_state == TimerState.WORK
        )

    def get_current_task_id(self):
        """
        Convenience method to get the current task id from the todoTasksList model
        """
        return self.task_interface.todoTasksList.model().currentTaskID()

    def get_current_task_index(self):
        """
        Convenience method to get the current task index from the todoTasksList model
        """
        return self.task_interface.todoTasksList.model().currentTaskIndex()

    def spawnTaskStartedInfoBar(self):
        if self.get_current_task_id() is None:
            return  # current task index can be None only when there is no tasks in todo list since when timer starts
        # a task would be automatically selected as the current task if any number of tasks other than zero are present
        # in the todo list

        # get name of task by its ID
        current_task_name = self.task_interface.todoTasksList.model().getTaskNameById(self.get_current_task_id())

        if not self.pomodoro_interface.pauseResumeButton.isChecked():
            InfoBar.success(
                title="Task Started",
                content=f'Task named "{current_task_name}" has started',
                orient=Qt.Orientation.Vertical,
                isClosable=True,
                duration=5000,
                position=InfoBarPosition.TOP_RIGHT,
                parent=self,
            )

    def check_current_task_deleted(self, task_id):
        if self.get_current_task_id() is not None and self.get_current_task_id() == task_id:
            self.task_interface.todoTasksList.model().setCurrentTaskID(None)
            if self.pomodoro_interface.pomodoro_timer_obj.getTimerState() in [
                TimerState.WORK,
                TimerState.BREAK,
                TimerState.LONG_BREAK,
            ]:
                # make sure that the current task is deleted and the timer is running, without timer being running
                # there is no need to show infobar
                InfoBar.warning(
                    title="Current Task Deleted",
                    content="The task you were working on has been deleted.\n"
                    "Select another task as soon as possible to save your progress."
                    if self.task_interface.todoTasksList.model().rowCount() > 0
                    else "The task you were working on has been deleted.\n"
                    "Select another task as soon as possible to save your progress.",
                    orient=Qt.Orientation.Vertical,
                    isClosable=True,
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=5000,
                    parent=self,
                )
                logger.debug("Current Task has been deleted")

    def check_current_task_moved(self, task_id, task_type: TaskType):
        if self.get_current_task_id() is not None:
            current_task_id = self.get_current_task_id()
        else:
            return  # no need to check if current task is moved if there is no current task

        if task_id == current_task_id and task_type == TaskType.COMPLETED:
            self.task_interface.todoTasksList.model().setCurrentTaskID(None)

            if self.pomodoro_interface.pomodoro_timer_obj.getTimerState() in [
                TimerState.WORK,
                TimerState.BREAK,
                TimerState.LONG_BREAK,
            ]:
                # make sure that the current task is moved into completed task list and the timer is running,
                # without timer being running there is no need to show infobar
                InfoBar.warning(
                    title="Current Task Completed",
                    content="The task you were working on has been completed.\n"
                    "Select another task as soon as possible to save your progress."
                    if self.task_interface.todoTasksList.model().rowCount() > 0
                    else "The task you were working on has been completed.\n"
                    "Add another task as soon as possible to save your progress.",
                    orient=Qt.Orientation.Vertical,
                    isClosable=True,
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=5000,
                    parent=self,
                )

            logger.debug("Current Task has been moved")

    def updateTaskTime(self):
        if self.get_current_task_id() is not None:
            if self.pomodoro_interface.pomodoro_timer_obj.getTimerState() in [TimerState.BREAK, TimerState.LONG_BREAK]:
                return

            final_elapsed_time = (
                self.task_interface.todoTasksList.model().data(
                    self.get_current_task_index(), TaskListModel.ElapsedTimeRole
                )
                + self.pomodoro_interface.pomodoro_timer_obj.timer_resolution
            )
            if final_elapsed_time % 1000 == 0:  # only update db when the elapsed time is a multiple of 1000
                self.task_interface.todoTasksList.model().setData(
                    self.get_current_task_index(), final_elapsed_time, TaskListModel.ElapsedTimeRole, update_db=False
                )
            if final_elapsed_time % 5000 == 0:
                self.updateTaskTimeDB()

    def updateTaskTimeDB(self):
        # since sessionStoppedSignal is emitted when the timer is stopped, we have to check if the current task index
        # is valid or not. Current Task Index can be invalid due to it being None when there are no tasks in todo list
        # when timer began or when current task is deleted and session is stopped automatically
        current_task_index = self.get_current_task_id()
        if current_task_index is None:
            return

        final_elapsed_time = self.task_interface.todoTasksList.model().data(
            self.get_current_task_index(), TaskListModel.ElapsedTimeRole
        )
        self.task_interface.todoTasksList.model().setData(
            self.get_current_task_index(), final_elapsed_time, TaskListModel.ElapsedTimeRole, update_db=True
        )
        logger.debug(f"Updated DB with elapsed time: {final_elapsed_time}")

    def connectSignalsToSlots(self):
        self.pomodoro_interface.pomodoro_timer_obj.timerStateChangedSignal.connect(
            self.toggleUIElementsBasedOnTimerState
        )
        self.pomodoro_interface.pomodoro_timer_obj.timerStateChangedSignal.connect(self.toggle_website_filtering)
        # Auto set current task whenever a work session begins. current task won't be overwritten if it is already set
        self.pomodoro_interface.pomodoro_timer_obj.timerStateChangedSignal.connect(
            lambda timerState: self.task_interface.autoSetCurrentTaskID() if timerState == TimerState.WORK else None
        )
        self.pomodoro_interface.pauseResumeButton.clicked.connect(self.spawnTaskStartedInfoBar)
        self.pomodoro_interface.pomodoro_timer_obj.pomodoro_timer.timeout.connect(self.updateTaskTime)
        self.task_interface.completedTasksList.model().taskMovedSignal.connect(self.check_current_task_moved)
        self.pomodoro_interface.pomodoro_timer_obj.sessionStoppedSignal.connect(self.updateTaskTimeDB)
        self.task_interface.todoTasksList.model().taskDeletedSignal.connect(self.check_current_task_deleted)
        self.pomodoro_interface.pomodoro_timer_obj.durationSkippedSignal.connect(self.updateTaskTimeDB)
        self.pomodoro_interface.pomodoro_timer_obj.sessionPausedSignal.connect(self.updateTaskTimeDB)
        self.website_filter_interface.blockTypeComboBox.currentIndexChanged.connect(
            lambda: self.toggle_website_filtering(self.pomodoro_interface.pomodoro_timer_obj.getTimerState())
        )
        self.website_filter_interface.saveButton.clicked.connect(
            lambda: self.toggle_website_filtering(self.pomodoro_interface.pomodoro_timer_obj.getTimerState())
        )  # todo: check if the list has changed before restarting the filtering
        self.workplace_list_model.current_workspace_changed.connect(load_workspace_settings)
        self.workplace_list_model.current_workspace_changed.connect(
            self.website_filter_interface.onCurrentWorkspaceChanged
        )
        self.workplace_list_model.current_workspace_changed.connect(
            self.task_interface.onCurrentWorkspaceChanged  # update task list when workspace is changed
        )
        self.pomodoro_interface.pomodoro_timer_obj.pomodoro_timer.timeout.connect(self.update_bottom_bar_timer_label)
        self.pomodoro_interface.pomodoro_timer_obj.timerStateChangedSignal.connect(self.update_bottom_bar_timer_label)
        workspace_specific_settings.enable_website_filter.valueChanged.connect(
            self.on_website_filter_enabled_setting_changed
        )
        workspace_specific_settings.enable_website_filter.valueChanged.connect(
            lambda: self.toggle_website_filtering(self.pomodoro_interface.pomodoro_timer_obj.getTimerState())
        )
        self.stackedWidget.mousePressEvent = self.onStackedWidgetClicked
        self.settings_interface.proxy_port_card.valueChanged.connect(self.update_proxy_port)
        # Sync pomodoro view button state with bottom bar button
        self.pomodoro_interface.pauseResumeButton.clicked.connect(lambda: self.syncBottomBarPauseResumeButton())
        self.pomodoro_interface.pomodoro_timer_obj.sessionStoppedSignal.connect(
            lambda: self.changeBottomBarPauseResumeButtonCheckedState(True)
        )
        self.pomodoro_interface.pomodoro_timer_obj.waitForUserInputSignal.connect(
            lambda: self.changeBottomBarPauseResumeButtonCheckedState(True)
        )
        self.pomodoro_interface.pomodoro_timer_obj.durationSkippedSignal.connect(
            lambda: self.changeBottomBarPauseResumeButtonCheckedState(False)
        )
        self.task_interface.todoTasksList.model().currentTaskChangedSignal.connect(
            lambda task_id: self.bottomBar.taskLabel.setText(
                f"Current Task: {self.task_interface.todoTasksList.model().getTaskNameById(task_id)}"
            )
        )
        self.themeListener.systemThemeChanged.connect(self.updateSystemTrayIcon)
        # for system tray
        self.pomodoro_interface.pomodoro_timer_obj.timerStateChangedSignal.connect(self.updateSystemTrayActions)
        # for notifications
        self.pomodoro_interface.pomodoro_timer_obj.timerStateChangedSignal.connect(self.showNotifications)

    def on_website_filter_enabled_setting_changed(self):
        enable_website_filter_setting_value = ConfigValues.ENABLE_WEBSITE_FILTER

        self.website_filter_interface.setEnabled(enable_website_filter_setting_value)

    def onStackedWidgetClicked(self, event):
        if self.stackedWidget.currentIndex() == 2 and not self.website_filter_interface.isEnabled():
            # show an infobar to inform the user that website filter is disabled and how it can be enabled
            InfoBar.warning(
                title="Website Filter is Disabled",
                content="You can enable the website filter from the settings view",
                orient=Qt.Orientation.Vertical,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=5000,
                parent=self,
            )

    def update_proxy_port(self):
        self.website_blocker_manager.proxy.port = ConfigValues.PROXY_PORT

    def update_bottom_bar_timer_label(self):
        # check if timer is running
        current_timer_state = self.pomodoro_interface.pomodoro_timer_obj.getTimerState()
        if current_timer_state in [TimerState.WORK, TimerState.BREAK, TimerState.LONG_BREAK]:
            # timer is running

            total_session_length_ms = 0
            if current_timer_state == TimerState.WORK:
                total_session_length_ms = ConfigValues.WORK_DURATION * 60 * 1000
            elif current_timer_state == TimerState.BREAK:
                total_session_length_ms = ConfigValues.BREAK_DURATION * 60 * 1000
            elif current_timer_state == TimerState.LONG_BREAK:
                total_session_length_ms = ConfigValues.LONG_BREAK_DURATION * 60 * 1000

            remaining_time_ms = self.pomodoro_interface.pomodoro_timer_obj.remaining_time

            if remaining_time_ms <= 0:  # have to compensate that the first second is not shown
                remaining_time_ms = total_session_length_ms

            hh, mm, ss = convert_ms_to_hh_mm_ss(remaining_time_ms)
            t_hh, t_mm, t_ss = convert_ms_to_hh_mm_ss(total_session_length_ms)

            timer_text = f"{current_timer_state.value}\n{hh:02d}:{mm:02d}:{ss:02d} / {t_hh:02d}:{t_mm:02d}:{t_ss:02d}"
            self.bottomBar.timerLabel.setText(timer_text)
            self.tray_menu_timer_status_action.setText(timer_text)

        else:
            # timer is not running
            hh, mm, ss = 0, 0, 0
            t_hh, t_mm, t_ss = 0, 0, 0

            timer_text = f"Timer is not running\n{hh:02d}:{mm:02d}:{ss:02d} / {t_hh:02d}:{t_mm:02d}:{t_ss:02d}"
            self.bottomBar.timerLabel.setText(timer_text)
            self.tray_menu_timer_status_action.setText(timer_text)

    def check_first_run(self):
        settings_dir_path = Path(settings_dir)
        first_run_dotfile_path = settings_dir_path.joinpath(FIRST_RUN_DOTFILE_NAME)

        if not first_run_dotfile_path.exists():
            logger.debug("First run detected")

            # create the first run dotfile
            first_run_dotfile_path.touch()

            return True

            # self.setupMitmproxy()

        return False

    def setupMitmproxy(self):
        logger.debug("Setting up mitmproxy")
        self.temporary_website_blocker_manager = WebsiteBlockerManager()
        self.temporary_website_blocker_manager.start_filtering(
            listening_port=ConfigValues.PROXY_PORT,
            joined_addresses="example.com",
            block_type="blocklist",
            mitmdump_bin_path=get_mitmdump_path(),
        )

        # setupAppDialog is a modal dialog, so it will block the main window until it is closed
        self.setupAppDialog = SetupAppDialog(parent=self.window())
        self.setupAppDialog.accepted.connect(lambda: self.giveGuidedTour())

    def giveGuidedTour(self):
        self.temporary_website_blocker_manager.stop_filtering(delete_proxy=True)  # stopping website filtering here
        # because this function will only be triggered after self.setupAppDialog is closed

        # todo: give a guided tour of the app to the user

        if ConfigValues.CHECK_FOR_UPDATES_ON_START:
            self.handleUpdates()  # added self.checkForUpdates here so that it is called after the setup dialog
            # is closed

    def handleUpdates(self):
        update_check_result = checkForUpdates()
        if update_check_result == UpdateCheckResult.UPDATE_AVAILABLE:
            # making the updateDialog
            self.updateDialog = UpdateDialog(parent=self.window())

            # for first run, the control flow is like this
            # self.setupMitmproxy() ---MainWindow is show---> self.setupAppDialog.show() ---
            # ---setupAppDialog is closed---> self.giveGuidedTour()  ---> self.checkForUpdates()

            # for runs which aren't first run, self.setupMitmproxy() is not run, so self.updateDialog is shown
            # when MainWindow is shown, in self.showEvent()
            if self.is_first_run and self.updateDialog is not None:
                self.updateDialog.show()

        elif update_check_result == UpdateCheckResult.UP_TO_DATE:
            pass

        elif update_check_result == UpdateCheckResult.NETWORK_UNREACHABLE:
            InfoBar.error(
                title="Update Check Failed",
                content="Failed to check for updates: Network is unreachable",
                orient=Qt.Orientation.Vertical,
                isClosable=True,
                duration=5000,
                position=InfoBarPosition.TOP_RIGHT,
                parent=self.window(),
            )

    def showEvent(self, event):
        logger.debug("MainWindow showEvent")
        super().showEvent(event)
        if self.is_first_run and self.setupAppDialog is not None:
            self.setupAppDialog.show()
        else:
            if self.updateDialog is not None:
                self.updateDialog.show()

    def closeEvent(self, event):
        self.website_blocker_manager.stop_filtering(delete_proxy=True)
        self.themeListener.terminate()
        self.themeListener.deleteLater()
        event.accept()
