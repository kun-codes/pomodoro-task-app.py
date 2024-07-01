import sys

from PySide6.QtWidgets import QWidget, QApplication

from src.views.tasks_view import TaskListView
# from src.ui.converted.task_card_ui import Ui_Form as TaskCardUi

from qfluentwidgets import FluentIcon, FluentWindow, setTheme, Theme

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.task_interface = TaskListView()


        self.initNavigation()
        self.initWindow()

    def initNavigation(self):

        # Add sub interface
        self.addSubInterface(self.task_interface, FluentIcon.ADD, 'Tasks')

    def initWindow(self):
        self.resize(1000, 800)
        self.setWindowTitle('Pomodoro Task List App')

if __name__ == '__main__':
    setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
