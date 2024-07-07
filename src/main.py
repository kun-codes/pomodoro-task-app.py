import sys

from PySide6.QtWidgets import QWidget, QApplication

from views.tasks_view import TaskListView
from views.pomodoro_view import PomodoroView
from views.settings_view import SettingsView
from models.drag_and_drop import DragWidget, DragItem
# from src.ui.converted.task_card_ui import Ui_Form as TaskCardUi

from qfluentwidgets import FluentIcon, FluentWindow, setTheme, Theme, NavigationItemPosition


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.task_interface = TaskListView()
        self.task_interface.setObjectName('task_interface')

        self.pomodoro_interface = PomodoroView()
        self.pomodoro_interface.setObjectName('pomodoro_interface')

        self.settings_interface = SettingsView()
        self.settings_interface.setObjectName('settings_interface')

        self.initNavigation()
        self.initWindow()
        self.populateTasks()

    def initNavigation(self):
        # Add sub interface
        self.addSubInterface(self.task_interface, FluentIcon.ADD, 'Tasks')
        self.addSubInterface(self.pomodoro_interface, FluentIcon.STOP_WATCH, 'Pomodoro')

        # Add sub interface at bottom
        self.addSubInterface(
            self.settings_interface, FluentIcon.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(1000, 800)
        self.setWindowTitle('Pomodoro Task List App')

    def populateTasks(self):
        for n, l in enumerate(["A1", "B1", "C1", "D1"]):
            item = DragItem(parent=self.task_interface.todoTasksCard, task_name=l)
            item.set_data(n)  # Store the data.
            self.task_interface.todoTasksCard.add_item(item)

        for n, l in enumerate(["A3", "B3", "C3", "D3"]):
            item = DragItem(parent=self.task_interface.completedTasksCard, task_name=l)
            item.set_data(n)  # Store the data.
            self.task_interface.completedTasksCard.add_item(item)



if __name__ == '__main__':
    setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
