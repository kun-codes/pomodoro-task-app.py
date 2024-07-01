from PySide6.QtGui import QColor
from PySide6.QtWidgets import QHBoxLayout, QApplication
from qfluentwidgets import CardWidget, BodyLabel, FluentIcon, isDarkTheme


# TaskCard is a simple card widget that displays a task along with an icon of its own
class TaskCard(CardWidget):
    def __init__(self, parent=None, task_name=""):
        super().__init__(parent=parent)
        self.setAcceptDrops(True)

        # TODO: See if icon is needed else remove it
        self.iconLabel = BodyLabel(self)
        self.iconLabel.setObjectName("iconLabel")
        self.iconLabel.setFixedSize(24, 24)
        self.iconLabel.setPixmap(FluentIcon.ADD.icon().pixmap(24, 24))

        self.taskLabel = BodyLabel(self)
        self.taskLabel.setObjectName("taskLabel")
        self.taskLabel.setText(task_name)

        self.layout = QHBoxLayout(self)

        self.layout.addWidget(self.iconLabel)
        self.layout.addWidget(self.taskLabel)

        self.setObjectName("taskCard")

    # Experimental
    def drag(self, event):
        self.setBackgroundColor(QColor(255, 255, 255, 13 if isDarkTheme() else 170))
        event.accept()


if __name__ == "__main__":
    app = QApplication([])
    w = TaskCard(task_name="Hello World")
    w.show()

    app.exec()
