from PySide6.QtWidgets import QWidget

from qfluentwidgets import FluentIcon, MessageBoxBase

from src.ui_py.ui_tasks_list_view import Ui_TaskView
from src.prefabs.addTaskDialog import AddTaskDialog


class TaskListView(QWidget, Ui_TaskView):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # set icons of buttons
        self.addTaskButton.setIcon(FluentIcon.ADD)
        self.addTaskButton.clicked.connect(self.addTask)

    def addTask(self):
        dialog = AddTaskDialog(self)
        dialog.show()

