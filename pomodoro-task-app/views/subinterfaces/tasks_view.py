from PySide6.QtCore import Qt, QModelIndex
from PySide6.QtWidgets import QWidget, QApplication, QSizePolicy, QAbstractItemView, QVBoxLayout
from qfluentwidgets import FluentIcon, TitleLabel, ListView, SimpleCardWidget
from loguru import logger

from models.db_tables import TaskType
from models.drag_and_drop import DragItem
from models.task_list_model import TaskListModel
from ui_py.ui_tasks_list_view import Ui_TaskView
from views.dialogs.addTaskDialog import AddTaskDialog


class TaskList(ListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setAutoScroll(True)


class TaskListView(Ui_TaskView, QWidget):
    """
    For tasks view of the app
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initLayout()
        self.setupSelectionBehavior()

    def initLayout(self):
        label_size_policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        self.todoTasksLabel = TitleLabel()
        self.todoTasksLabel.setText("Todo Tasks")
        self.todoTasksLabel.setSizePolicy(label_size_policy)
        self.scrollAreaWidgetContents.layout().addWidget(self.todoTasksLabel)

        # card inside which todo tasks list will be kept
        self.todoTasksCard = SimpleCardWidget()
        self.todoTasksCard.setLayout(QVBoxLayout())
        self.scrollAreaWidgetContents.layout().addWidget(self.todoTasksCard)

        self.todoTasksList = TaskList(self.todoTasksCard)
        self.todoTasksList.setModel(TaskListModel(TaskType.TODO))
        self.todoTasksList.setObjectName("todoTasksList")
        self.todoTasksCard.layout().addWidget(self.todoTasksList)

        self.completedTasksLabel = TitleLabel()
        self.completedTasksLabel.setText("Completed Tasks")
        self.completedTasksLabel.setSizePolicy(label_size_policy)
        self.scrollAreaWidgetContents.layout().addWidget(self.completedTasksLabel)

        # card inside which completed tasks list will be kept
        self.completedTasksCard = SimpleCardWidget()
        self.completedTasksCard.setLayout(QVBoxLayout())
        self.scrollAreaWidgetContents.layout().addWidget(self.completedTasksCard)

        self.completedTasksList = TaskList(self)
        self.completedTasksList.setModel(TaskListModel(TaskType.COMPLETED))
        self.completedTasksList.setObjectName("completedTasksList")
        self.completedTasksCard.layout().addWidget(self.completedTasksList)

        # set icons of buttons
        self.addTaskButton.setIcon(FluentIcon.ADD)
        self.addTaskButton.clicked.connect(self.addTask)

    def addTask(self):
        dialog = AddTaskDialog(self)
        # if user clicks on add task inside dialog
        if dialog.exec():
            task_name = dialog.taskEdit.text()
            row = self.todoTasksList.model().rowCount(QModelIndex())
            self.todoTasksList.model().insertRow(row, QModelIndex(), task_name=task_name, task_type=TaskType.TODO)

    def setupSelectionBehavior(self):
        """
        To ensure that only one item is selected out of both the lists
        """
        self.todoTasksList.selectionModel().selectionChanged.connect(self.onTodoTasksSelectionChanged)
        self.completedTasksList.selectionModel().selectionChanged.connect(self.onCompletedTasksSelectionChanged)

    def onTodoTasksSelectionChanged(self):
        if self.todoTasksList.selectionModel().hasSelection():
            # disconnecting and connecting again so that the other SelectionChanged method is not called
            # when selection is cleared
            self.completedTasksList.selectionModel().selectionChanged.disconnect(self.onCompletedTasksSelectionChanged)
            self.completedTasksList.clearSelection()
            self.completedTasksList.selectionModel().selectionChanged.connect(self.onCompletedTasksSelectionChanged)

    def onCompletedTasksSelectionChanged(self):
        if self.completedTasksList.selectionModel().hasSelection():
            # disconnecting and connecting again so that the other SelectionChanged method is not called
            # when selection is cleared
            self.todoTasksList.selectionModel().selectionChanged.disconnect(self.onTodoTasksSelectionChanged)
            self.todoTasksList.clearSelection()
            self.todoTasksList.selectionModel().selectionChanged.connect(self.onTodoTasksSelectionChanged)

    def onCurrentWorkspaceChanged(self):
        self.todoTasksList.model().load_data()
        self.completedTasksList.model().load_data()


if __name__ == "__main__":
    app = QApplication()
    w = TaskListView()
    w.show()
    app.exec()
