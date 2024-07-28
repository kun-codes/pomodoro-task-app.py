from PySide6.QtCore import QAbstractListModel, Qt
from qfluentwidgets import FluentIcon

tick_icon = FluentIcon.ACCEPT.icon()
# tick_pixmap = tick_icon.pixmap(32, 32)
tick = tick_icon


# basedir = os.path.dirname(__file__)
# tick = QImage(os.path.join(basedir, "tick.png"))

class TasksModel(QAbstractListModel):
    def __init__(self):
        super().__init__()
        self.tasks = []

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            status, text = self.tasks[index.row()]
            return text

        if role == Qt.ItemDataRole.DecorationRole:
            status, text = self.tasks[index.row()]
            if status:
                return tick

    def rowCount(self, index):
        return len(self.tasks)
