from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QApplication, QSizePolicy

from qfluentwidgets import FluentIcon, MessageBoxBase, TitleLabel

from ui_py.ui_tasks_list_view import Ui_TaskView
from prefabs.addTaskDialog import AddTaskDialog
from models.drag_and_drop import DragWidget


class TaskListView(QWidget, Ui_TaskView):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        label_size_policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        self.todoTasksLabel = TitleLabel()
        self.todoTasksLabel.setText("Todo Tasks")
        self.todoTasksLabel.setSizePolicy(label_size_policy)
        self.scrollAreaWidgetContents.layout().addWidget(self.todoTasksLabel)

        # Add the todoTasksCard to the taskListView
        self.todoTasksCard = DragWidget(Qt.Orientation.Vertical)
        self.scrollAreaWidgetContents.layout().addWidget(self.todoTasksCard)
        self.todoTasksCard.setObjectName("todoTasksCard")
        self.todoTasksCard.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

        self.completedTasksLabel = TitleLabel()
        self.completedTasksLabel.setText("Completed Tasks")
        self.completedTasksLabel.setSizePolicy(label_size_policy)
        self.scrollAreaWidgetContents.layout().addWidget(self.completedTasksLabel)

        # Add the completedTasksCard to the taskListView
        self.completedTasksCard = DragWidget(Qt.Orientation.Vertical)
        self.scrollAreaWidgetContents.layout().addWidget(self.completedTasksCard)
        self.completedTasksCard.setObjectName("completedTasksCard")
        self.completedTasksCard.layout().setAlignment(Qt.AlignmentFlag.AlignTop)


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