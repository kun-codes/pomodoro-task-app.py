import json
import os

from PySide6.QtWidgets import QMainWindow

from src.models.tasks_model import TasksModel
from src.ui.converted.tasks_ui import Ui_MainWindow

TASKS_FILE_LOCATION = "../data/data.json"

if not os.path.exists(TASKS_FILE_LOCATION):
    os.makedirs(os.path.dirname(TASKS_FILE_LOCATION))

class TasksView(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # setTheme(Theme.LIGHT)

        self.setStyleSheet("TasksView{background: rgb(255,255,255)}")

        self.model = TasksModel()
        self.load()
        self.todoView.setModel(self.model)

        self.addButton.pressed.connect(self.add)
        self.deleteButton.pressed.connect(self.delete)
        self.completedButton.pressed.connect(self.complete)

    def add(self):
        text = self.todoEdit.text()
        text = text.strip()
        if text:  # Don't add empty strings.
            self.model.tasks.append((False, text))
            self.model.layoutChanged.emit()
            self.todoEdit.setText("")
            self.save()

    def delete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            index = indexes[0]
            del self.model.tasks[index.row()]
            self.model.layoutChanged.emit()
            self.todoView.clearSelection()
            self.save()

    def complete(self):
        indexes = self.todoView.selectedIndexes()
        if indexes:
            index = indexes[0]
            row = index.row()
            status, text = self.model.tasks[row]
            self.model.tasks[row] = (True, text)
            # .dataChanged takes top-left and bottom right, which are equal
            # for a single selection.
            self.model.dataChanged.emit(index, index)
            self.todoView.clearSelection()
            self.save()

    def load(self):
        try:
            with open(TASKS_FILE_LOCATION, "r") as f:
                self.model.tasks = json.load(f)
        except Exception:
            pass

    def save(self):
        with open(TASKS_FILE_LOCATION, "w") as f:
            data = json.dump(self.model.tasks, f)
