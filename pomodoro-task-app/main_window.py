from qfluentwidgets import FluentIcon, FluentWindow, NavigationItemPosition

from models.drag_and_drop import DragItem
from models.timer import TimerState
from views.dialogs.workplaceManagerDialog import ManageWorkspaceDialog
from views.subinterfaces.pomodoro_view import PomodoroView
from views.subinterfaces.settings_view import SettingsView
from views.subinterfaces.tasks_view import TaskListView


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.task_interface = TaskListView()
        self.task_interface.setObjectName('task_interface')

        self.pomodoro_interface = PomodoroView()
        self.pomodoro_interface.setObjectName('pomodoro_interface')

        self.settings_interface = SettingsView()
        self.settings_interface.setObjectName('settings_interface')

        self.pomodoro_interface.pomodoro_timer_obj.timerStateChangedSignal.connect(
            self.disablePomodoroSettingsDuringTimer)

        self.initNavigation()
        self.initWindow()
        self.populateTasks()

    def initNavigation(self):
        # Add sub interface
        self.addSubInterface(self.task_interface, FluentIcon.ADD, 'Tasks')
        self.addSubInterface(self.pomodoro_interface, FluentIcon.STOP_WATCH, 'Pomodoro')

        # Add sub interface at bottom
        self.navigationInterface.addItem(
            routeKey="WorkplaceSelector",
            icon=FluentIcon.VPN,
            text="Select Workplace",
            onClick=lambda: self.onWorkplaceManagerClicked(),
            selectable=False,
            tooltip="Select the workplace to work on",
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

    def onWorkplaceManagerClicked(self):
        # parent is set according to: https://pyqt-fluent-widgets.readthedocs.io/en/latest/navigation.html
        dialog = ManageWorkspaceDialog(parent=self.stackedWidget)
        dialog.exec()

    def disablePomodoroSettingsDuringTimer(self, timerState):
        # TODO: show a tip to stop the timer before changing settings when timer is running
        if timerState in [TimerState.WORK, TimerState.BREAK, TimerState.LONG_BREAK]:
            self.settings_interface.pomodoro_settings_group.setDisabled(True)
        else:
            self.settings_interface.pomodoro_settings_group.setDisabled(False)
