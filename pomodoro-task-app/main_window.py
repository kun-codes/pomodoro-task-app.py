from qfluentwidgets import FluentIcon, FluentWindow, NavigationItemPosition, InfoBar, InfoBarPosition
from loguru import logger
from PySide6.QtCore import Qt

from constants import WebsiteFilterType, URLListType
from config_values import ConfigValues
from models.task_list_model import TaskListModel
from models.timer import TimerState
from views.dialogs.workspaceManagerDialog import ManageWorkspaceDialog
from views.subinterfaces.pomodoro_view import PomodoroView
from views.subinterfaces.settings_view import SettingsView
from views.subinterfaces.tasks_view import TaskListView
from views.subinterfaces.website_blocker_view import WebsiteBlockerView
from models.db_tables import Workspace, CurrentWorkspace, TaskType, Task
from utils.db_utils import get_session
from models.workspace_list_model import WorkspaceListModel
from models.config import load_workspace_settings
from website_blocker.website_blocker_manager import WebsiteBlockerManager
from utils.find_mitmdump_executable import get_mitmdump_path
from prefabs.customFluentIcon import CustomFluentIcon


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()

        self.check_valid_db()

        self.workplace_list_model = WorkspaceListModel()

        self.task_interface = TaskListView()
        self.task_interface.setObjectName('task_interface')

        self.pomodoro_interface = PomodoroView()
        self.pomodoro_interface.setObjectName('pomodoro_interface')

        self.settings_interface = SettingsView()
        self.settings_interface.setObjectName('settings_interface')

        self.website_filter_interface = WebsiteBlockerView(self.workplace_list_model)
        self.website_filter_interface.setObjectName('website_filter_interface')

        self.manage_workspace_dialog = None

        self.website_blocker_manager = WebsiteBlockerManager()

        self.current_task_index = None
        self.already_elapsed_time = 0

        self.connectSignalsToSlots()
        self.initNavigation()
        self.initWindow()

        self.navigationInterface.panel.setFixedHeight(48)

    def initNavigation(self):
        # Add sub interface
        self.addSubInterface(self.task_interface, CustomFluentIcon.TASKS_VIEW, 'Tasks')
        self.addSubInterface(self.pomodoro_interface, FluentIcon.STOP_WATCH, 'Pomodoro')
        self.addSubInterface(self.website_filter_interface, CustomFluentIcon.WEBSITE_FILTER_VIEW, 'Website Filter')

        # Add sub interface at bottom
        self.navigationInterface.addItem(
            routeKey="WorkspaceSelector",
            icon=CustomFluentIcon.WORKSPACE_SELECTOR_VIEW,
            text="Select Workspace",
            onClick=lambda: self.onWorkspaceManagerClicked(),
            selectable=False,
            tooltip="Select the workspace to work in",
            position=NavigationItemPosition.BOTTOM
        )
        self.addSubInterface(
            self.settings_interface, FluentIcon.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(1000, 800)
        self.setWindowTitle('Pomodoro Task List App')

    def onWorkspaceManagerClicked(self):
        if self.manage_workspace_dialog is None:
            self.manage_workspace_dialog = ManageWorkspaceDialog(parent=self.window(), workspaceListModel=self.workplace_list_model)

        self.manage_workspace_dialog.show()

    def toggleUIElementsBasedOnTimerState(self, timerState):
        # TODO: show a tip to stop the timer before changing settings when timer is running
        workspace_selector_button = self.navigationInterface.panel.widget("WorkspaceSelector")
        if timerState in [TimerState.WORK, TimerState.BREAK, TimerState.LONG_BREAK]:
            self.settings_interface.pomodoro_settings_group.setDisabled(True)
            workspace_selector_button.setDisabled(True)
        else:
            self.settings_interface.pomodoro_settings_group.setDisabled(False)
            workspace_selector_button.setDisabled(False)

    def toggle_website_filtering(self, timerState):
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
            logger.debug("Starting website filtering")
            self.website_blocker_manager.start_filtering(8080, joined_urls, block_type, mitmdump_path)
        else:
            logger.debug("Stopping website filtering")
            self.website_blocker_manager.stop_filtering(delete_proxy=True)

    def is_task_beginning(self):
        current_state = self.pomodoro_interface.pomodoro_timer_obj.getTimerState()
        previous_state = self.pomodoro_interface.pomodoro_timer_obj.previous_timer_state

        return previous_state in [TimerState.NOTHING, TimerState.BREAK, TimerState.LONG_BREAK] and \
            current_state == TimerState.WORK


    def store_current_task(self):
        self.current_task_index = self.task_interface.currentTaskIndex()

    def spawnTaskStartedInfoBar(self):
        current_task_name = self.current_task_index.data(Qt.DisplayRole)
        if not self.pomodoro_interface.pauseResumeButton.isChecked():
            InfoBar.success(
                title="Task Started",
                content=f'Task named "{current_task_name}" has started',
                isClosable=True,
                duration=5000,
                position=InfoBarPosition.TOP_RIGHT,
                parent=self
            )

    def store_already_elapsed_time(self):
        logger.debug("Storing already elapsed time")
        if self.current_task_index is not None and self.is_task_beginning():
            elapsed_time = self.current_task_index.data(TaskListModel.ElapsedTimeRole)
            self.already_elapsed_time = elapsed_time

    def check_current_task_deleted(self, task_index):
        if self.current_task_index is not None and self.current_task_index == task_index and \
            self.pomodoro_interface.pomodoro_timer_obj.getTimerState() in \
                [TimerState.WORK, TimerState.BREAK, TimerState.LONG_BREAK]:
            # make sure that the current task is deleted and the timer is running, without timer being running
            # there is no need to stop the timer and show infobar
            self.pomodoro_interface.pomodoro_timer_obj.stopSession()
            self.current_task_index = None
            self.already_elapsed_time = 0
            InfoBar.warning(
                title="Pomodoro Timer Stopped",
                content="The task you were working on has been deleted. Please select another task to continue." \
                        if self.task_interface.todoTasksList.model().rowCount() > 0 else
                            "The task you were working on has been deleted. Please add a new task to continue.",
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=5000,
                parent = self
            )
            logger.debug("Current Task has been deleted")

    def check_current_task_moved(self, task_id, task_type:TaskType):
        if self.current_task_index is not None:
            current_task_id = self.current_task_index.data(TaskListModel.IDRole)
        else:
            return  # no need to check if current task is moved if there is no current task

        if (task_id == current_task_id and task_type == TaskType.COMPLETED and
                self.pomodoro_interface.pomodoro_timer_obj.getTimerState() in
                [TimerState.WORK, TimerState.BREAK, TimerState.LONG_BREAK]):
            # make sure that the current task is moved into completed task list and the timer is running,
            # without timer being running there is no need to stop the timer and show infobar
            self.pomodoro_interface.pomodoro_timer_obj.stopSession()
            self.current_task_index = None
            self.already_elapsed_time = 0
            InfoBar.warning(
                title="Pomodoro Timer Stopped",
                content="The task you were working on has been completed. Please select another task to continue." \
                    if self.task_interface.todoTasksList.model().rowCount() > 0 else
                "The task you were working on has been completed. Please add a new task to continue.",
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=5000,
                parent = self
            )
            logger.debug("Current Task has been moved")

    def updateTaskTime(self):
        if self.current_task_index is not None:
            if self.pomodoro_interface.pomodoro_timer_obj.getTimerState() == TimerState.WORK:
                duration = ConfigValues.WORK_DURATION * 60 * 1000  ## in ms
            elif self.pomodoro_interface.pomodoro_timer_obj.getTimerState() in [TimerState.BREAK, TimerState.LONG_BREAK]:
                return

            remaining_duration = self.pomodoro_interface.pomodoro_timer_obj.remaining_time
            elapsed_time = duration - remaining_duration

            final_elapsed_time = self.already_elapsed_time + elapsed_time
            if final_elapsed_time % 1000 == 0:  # only update db when the elapsed time is a multiple of 1000
                self.task_interface.todoTasksList.model().setData(self.current_task_index, final_elapsed_time, TaskListModel.ElapsedTimeRole, update_db=False)
            if final_elapsed_time % 5000 == 0:
                self.updateTaskTimeDB()

    def updateTaskTimeDB(self):
        final_elapsed_time = self.task_interface.todoTasksList.model().data(self.current_task_index, TaskListModel.ElapsedTimeRole)
        self.task_interface.todoTasksList.model().setData(self.current_task_index, final_elapsed_time, TaskListModel.ElapsedTimeRole, update_db=True)
        logger.debug(f"Updated DB with elapsed time: {final_elapsed_time}")

    def connectSignalsToSlots(self):
        self.pomodoro_interface.pomodoro_timer_obj.timerStateChangedSignal.connect(
            self.toggleUIElementsBasedOnTimerState)
        self.pomodoro_interface.pomodoro_timer_obj.timerStateChangedSignal.connect(
            self.toggle_website_filtering
        )
        self.pomodoro_interface.pomodoro_timer_obj.timerStateChangedSignal.connect(
            self.store_current_task
        )
        self.pomodoro_interface.pomodoro_timer_obj.timerStateChangedSignal.connect(
            self.store_already_elapsed_time
        )
        self.pomodoro_interface.pauseResumeButton.clicked.connect(
            self.spawnTaskStartedInfoBar
        )
        self.pomodoro_interface.pomodoro_timer_obj.pomodoro_timer.timeout.connect(
            self.updateTaskTime
        )
        self.task_interface.todoTasksList.model().taskDeletedSignal.connect(
            self.check_current_task_deleted
        )
        self.task_interface.completedTasksList.model().taskMovedSignal.connect(
            self.check_current_task_moved
        )
        self.pomodoro_interface.pomodoro_timer_obj.sessionStoppedSignal.connect(
            self.updateTaskTimeDB
        )
        self.pomodoro_interface.pomodoro_timer_obj.durationSkippedSignal.connect(
            self.updateTaskTimeDB
        )
        self.pomodoro_interface.pomodoro_timer_obj.sessionPausedSignal.connect(
            self.updateTaskTimeDB
        )
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

    def check_valid_db(self):
        with get_session() as session:
            workspace = session.query(Workspace).first()
            # create a default workspace if none exists
            if not workspace:
                workspace = Workspace(workspace_name="Default Workspace")
                session.add(workspace)
                session.commit()

                # add some tasks too
                sample_tasks = [
                    Task(workspace_id=workspace.id, task_name="Sample Task 1", task_type=TaskType.TODO, task_position=1),
                    Task(workspace_id=workspace.id, task_name="Sample Task 2", task_type=TaskType.TODO, task_position=2),
                    Task(workspace_id=workspace.id, task_name="Sample Task 3", task_type=TaskType.TODO, task_position=3),
                    Task(workspace_id=workspace.id, task_name="Sample Task 4", task_type=TaskType.COMPLETED, task_position=4),
                    Task(workspace_id=workspace.id, task_name="Sample Task 5", task_type=TaskType.COMPLETED, task_position=5),
                    Task(workspace_id=workspace.id, task_name="Sample Task 6", task_type=TaskType.COMPLETED, task_position=6),
                ]
                session.add_all(sample_tasks)
                session.commit()


            # if application was closed while no workspace was selected, select the first workspace in the database
            # if database had no workspace to begin with then set default workspace as current database
            current_workspace = session.query(CurrentWorkspace).first()
            if not current_workspace:
                current_workspace = CurrentWorkspace(current_workspace_id=workspace.id)
                session.add(current_workspace)
                session.commit()


    def closeEvent(self, event):
        self.website_blocker_manager.stop_filtering(delete_proxy=True)
        event.accept()
