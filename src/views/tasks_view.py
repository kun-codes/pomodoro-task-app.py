from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QApplication, QSizePolicy, QMainWindow

from qfluentwidgets import FluentIcon, MessageBoxBase, TitleLabel

from ui_py.ui_tasks_list_view import Ui_TaskView
from prefabs.addTaskDialog import AddTaskDialog
from models.drag_and_drop import DragWidget, DragItem


class TaskListView(Ui_TaskView, QWidget):
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
        self.todoTasksCard.setObjectName("todoTasksCard")
        self.scrollAreaWidgetContents.layout().addWidget(self.todoTasksCard)
        self.todoTasksCard.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

        self.completedTasksLabel = TitleLabel()
        self.completedTasksLabel.setText("Completed Tasks")
        self.completedTasksLabel.setSizePolicy(label_size_policy)
        self.scrollAreaWidgetContents.layout().addWidget(self.completedTasksLabel)

        # Add the completedTasksCard to the taskListView
        self.completedTasksCard = DragWidget(Qt.Orientation.Vertical)
        self.completedTasksCard.setObjectName("completedTasksCard")
        self.scrollAreaWidgetContents.layout().addWidget(self.completedTasksCard)
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
    for n, l in enumerate(["A1", "B1", "C1", "D1"]):
        item = DragItem(parent=w.todoTasksCard, task_name=l)
        item.set_data(n)  # Store the data.
        w.todoTasksCard.add_item(item)

    for n, l in enumerate(["A3", "B3", "C3", "D3"]):
        item = DragItem(parent=w.completedTasksCard, task_name=l)
        item.set_data(n)  # Store the data.
        w.completedTasksCard.add_item(item)
    w.show()
    app.exec()