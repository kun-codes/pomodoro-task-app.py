from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QApplication, QSizePolicy

from qfluentwidgets import FluentIcon, MessageBoxBase, TitleLabel

from src.ui_py.ui_tasks_list_view import Ui_TaskView
from src.prefabs.addTaskDialog import AddTaskDialog
from src.models.drag_and_drop import DragWidget


class TaskListView(QWidget, Ui_TaskView):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        label_size_policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        self.todoTasksLabel = TitleLabel("Todo Tasks")
        self.todoTasksLabel.setSizePolicy(label_size_policy)
        self.scrollAreaWidgetContents.layout().addWidget(self.todoTasksLabel)

        # Add the todoTasksCard to the taskListView
        self.todoTasksCard = DragWidget()
        self.scrollAreaWidgetContents.layout().addWidget(self.todoTasksCard)

        self.completedTasksLabel = TitleLabel("Completed Tasks")
        self.completedTasksLabel.setSizePolicy(label_size_policy)
        self.scrollAreaWidgetContents.layout().addWidget(self.completedTasksLabel)

        # Add the completedTasksCard to the taskListView
        self.completedTasksCard = DragWidget()
        self.scrollAreaWidgetContents.layout().addWidget(self.completedTasksCard)


        # set icons of buttons
        self.addTaskButton.setIcon(FluentIcon.ADD)
        self.addTaskButton.clicked.connect(self.addTask)

    def addTask(self):
        dialog = AddTaskDialog(self)
        dialog.show()


if __name__ == "__main__":

    app = QApplication()
    w = TaskListView()
    w.show()
    app.exec()