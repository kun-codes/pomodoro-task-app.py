import sys

from PySide6.QtWidgets import QWidget, QApplication

from src.views.tasks_view import TaskListView
from src.models.drag_and_drop import DragWidget, DragItem
# from src.ui.converted.task_card_ui import Ui_Form as TaskCardUi

from qfluentwidgets import FluentIcon, FluentWindow, setTheme, Theme


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.task_interface = TaskListView()

        self.initNavigation()
        self.initWindow()
        self.populateTasks()

    def initNavigation(self):
        # Add sub interface
        self.addSubInterface(self.task_interface, FluentIcon.ADD, 'Tasks')

    def initWindow(self):
        self.resize(1000, 800)
        self.setWindowTitle('Pomodoro Task List App')

    def populateTasks(self):
        for n, l in enumerate(["A1", "B1", "C1", "D1"]):
            item = DragItem(l)
            item.set_data(n)  # Store the data.
            self.task_interface.todoTasksCard.add_item(item)

        for n, l in enumerate(["A3", "B3", "C3", "D3"]):
            item = DragItem(l)
            item.set_data(n)  # Store the data.
            self.task_interface.completedTasksCard.add_item(item)



if __name__ == '__main__':
    setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
