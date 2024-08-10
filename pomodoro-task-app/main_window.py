from qfluentwidgets import FluentIcon, FluentWindow, NavigationItemPosition

from models.drag_and_drop import DragItem
from models.timer import TimerState
from views.dialogs.workspaceManagerDialog import ManageWorkspaceDialog
from views.subinterfaces.pomodoro_view import PomodoroView
from views.subinterfaces.settings_view import SettingsView
from views.subinterfaces.tasks_view import TaskListView
from views.subinterfaces.website_blocker_view import WebsiteBlockerView
from models.db_tables import engine, Workspace, CurrentWorkspace
from utils.db_utils import get_session
from models.workspace_list_model import WorkspaceListModel


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
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
            self.disablePomodoroSettingsDuringTimer)

        self.initNavigation()
        self.initWindow()
        self.populateTasks()
        self.check_valid_db()

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

    def populateTasks(self):
        for n, l in enumerate(["A1", "B1", "C1", "D1"]):
            item = DragItem(task_name=l)
            item.set_data(n)  # Store the data.
            self.task_interface.todoTasksCard.add_item(item)

        for n, l in enumerate(["A3", "B3", "C3", "D3"]):
            item = DragItem(task_name=l)
            item.set_data(n)  # Store the data.
            self.task_interface.completedTasksCard.add_item(item)

    def onWorkspaceManagerClicked(self):
        # parent is set according to: https://pyqt-fluent-widgets.readthedocs.io/en/latest/navigation.html
        dialog = ManageWorkspaceDialog(parent=self.stackedWidget, workspaceListModel=self.workplace_list_model)
        dialog.exec()

    def disablePomodoroSettingsDuringTimer(self, timerState):
        # TODO: show a tip to stop the timer before changing settings when timer is running
        if timerState in [TimerState.WORK, TimerState.BREAK, TimerState.LONG_BREAK]:
            self.settings_interface.pomodoro_settings_group.setDisabled(True)
        else:
            self.settings_interface.pomodoro_settings_group.setDisabled(False)

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
