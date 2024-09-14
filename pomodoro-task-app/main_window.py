from qfluentwidgets import FluentIcon, FluentWindow, NavigationItemPosition
from loguru import logger
from PySide6.QtCore import Qt

from constants import WebsiteFilterType, URLListType, WORK_DURATION
from models.drag_and_drop import DragItem
from models.task_list_model import TaskListModel
from models.timer import TimerState
from views.dialogs.workspaceManagerDialog import ManageWorkspaceDialog
from views.subinterfaces.pomodoro_view import PomodoroView
from views.subinterfaces.settings_view import SettingsView
from views.subinterfaces.tasks_view import TaskListView
from views.subinterfaces.website_blocker_view import WebsiteBlockerView
from models.db_tables import Workspace, CurrentWorkspace
from utils.db_utils import get_session
from models.workspace_list_model import WorkspaceListModel
from models.config import load_workspace_settings
from website_blocker.website_blocker_manager import WebsiteBlockerManager
from utils.find_mitmdump_executable import get_mitmdump_path


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

        self.pomodoro_interface.pomodoro_timer_obj.timerStateChangedSignal.connect(
            self.toggleUIElementsBasedOnTimerState)
        self.pomodoro_interface.pomodoro_timer_obj.timerStateChangedSignal.connect(
            self.toggle_website_filtering
        )
        self.pomodoro_interface.pauseResumeButton.clicked.connect(
            self.store_current_task
        )
        self.pomodoro_interface.pomodoro_timer_obj.pomodoro_timer.timeout.connect(
            self.updateTaskTime
        )

        self.manage_workspace_dialog = None

        self.website_blocker_manager = WebsiteBlockerManager()

        self.current_task = None
        self.already_elapsed_time = 0

        self.connectSignalsToSlots()
        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        # Add sub interface
        self.addSubInterface(self.task_interface, FluentIcon.ADD, 'Tasks')
        self.addSubInterface(self.pomodoro_interface, FluentIcon.STOP_WATCH, 'Pomodoro')
        self.addSubInterface(self.website_filter_interface, FluentIcon.VPN, 'Website Filter')

        # Add sub interface at bottom
        self.navigationInterface.addItem(
            routeKey="WorkspaceSelector",
            icon=FluentIcon.VPN,
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
            # parent is set according to: https://pyqt-fluent-widgets.readthedocs.io/en/latest/navigation.html
            self.manage_workspace_dialog = ManageWorkspaceDialog(parent=self.stackedWidget, workspaceListModel=self.workplace_list_model)

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
            joined_urls = "$[]".join(urls)

        mitmdump_path = get_mitmdump_path()

        if timerState == TimerState.WORK:
            logger.debug("Starting website filtering")
            self.website_blocker_manager.start_filtering(8080, joined_urls, block_type, mitmdump_path)
        else:
            logger.debug("Stopping website filtering")
            self.website_blocker_manager.stop_filtering()

    def store_current_task(self):
        self.current_task = self.task_interface.currentTaskIndex()
        self.already_elapsed_time, _ = self.current_task.data(Qt.UserRole)  # stores the already elapsed time of the current Task

    def updateTaskTime(self):
        work_duration = WORK_DURATION * 60 * 1000  ## in ms
        remaining_duration = self.pomodoro_interface.pomodoro_timer_obj.remaining_time
        elapsed_time = work_duration - remaining_duration

        final_elapsed_time = self.already_elapsed_time + elapsed_time
        logger.debug(f"Elapsed time: {final_elapsed_time}")
        if final_elapsed_time % 1000 == 0:  # only update db once a second
            self.task_interface.todoTasksList.model().updateTask(self.current_task.row(), elapsed_time=final_elapsed_time)

    def connectSignalsToSlots(self):
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

            # if application was closed while no workspace was selected, select the first workspace in the database
            # if database had no workspace to begin with then set default workspace as current database
            current_workspace = session.query(CurrentWorkspace).first()
            if not current_workspace:
                current_workspace = CurrentWorkspace(current_workspace_id=workspace.id)
                session.add(current_workspace)
                session.commit()
