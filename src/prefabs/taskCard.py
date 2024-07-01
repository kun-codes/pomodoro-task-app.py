from PySide6.QtWidgets import QHBoxLayout, QApplication
from qfluentwidgets import CardWidget, BodyLabel, FluentIcon

# TaskCard is a simple card widget that displays a task along with an icon of its own
class TaskCard(CardWidget):
    def __init__(self, parent=None, taskName=""):
        super().__init__(parent=parent)
        self.setAcceptDrops(True)

        # TODO: See if icon is needed else remove it
        self.iconLabel = BodyLabel(self)
        self.iconLabel.setObjectName("iconLabel")
        self.iconLabel.setFixedSize(24, 24)
        self.iconLabel.setPixmap(FluentIcon.ADD.icon().pixmap(24, 24))

        self.taskLabel = BodyLabel(self)
        self.taskLabel.setObjectName("taskLabel")
        self.taskLabel.setText(taskName)

        self.layout = QHBoxLayout(self)

        self.layout.addWidget(self.iconLabel)
        self.layout.addWidget(self.taskLabel)

        self.setObjectName("taskCard")

if __name__ == "__main__":
    app = QApplication([])
    w = TaskCard(taskName="Hello World")
    w.show()

    app.exec()
