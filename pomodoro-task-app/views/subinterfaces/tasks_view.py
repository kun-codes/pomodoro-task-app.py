from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QApplication, QSizePolicy
from qfluentwidgets import FluentIcon, TitleLabel

from models.drag_and_drop import DragWidget, DragItem
from views.dialogs.addTaskDialog import AddTaskDialog
from ui_py.ui_tasks_list_view import Ui_TaskView
from models.db_tables import Task, TaskType, engine
from utils.db_utils import get_session


class TaskListView(Ui_TaskView, QWidget):
    """
    For tasks view of the app
    """
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

        self.loadTasksFromDB()

    def loadTasksFromDB(self):
        # loading tasks from database of todo type
        with get_session(is_read_only=True) as session:
            tasks = session.query(Task).filter(Task.task_type == TaskType.TODO).all()
        for task in tasks:
            task_name = task.task_name
            task_card = DragItem(parent=self.todoTasksCard, task_name=task_name)
            self.todoTasksCard.add_item(task_card)

        # loading tasks from database of completed type
        with get_session(is_read_only=True) as session:
            tasks = session.query(Task).filter(Task.task_type == TaskType.COMPLETED).all()
        for task in tasks:
            task_name = task.task_name
            task_card = DragItem(parent=self.completedTasksCard, task_name=task_name)
            self.completedTasksCard.add_item(task_card)


    def addTask(self):
        dialog = AddTaskDialog(self)
        # if user clicks on add task inside dialog
        if dialog.exec():
            task_name = dialog.taskEdit.text()
            task_card = DragItem(parent=self.todoTasksCard, task_name=task_name)
            self.todoTasksCard.add_item(task_card)

            with get_session() as session:
                session.add(task_card.task_record)


    def addTaskCard(self, task_name: str):
        item = DragItem(parent=self.todoTasksCard, task_name=task_name)
        self.todoTasksCard.add_item(item)


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
