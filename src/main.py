import sys

from PySide6.QtWidgets import QApplication

from src.views.tasks_view import TasksView

app = QApplication(sys.argv)
window = TasksView()
window.show()
app.exec()
