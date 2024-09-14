from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray, QMimeData, QDataStream, QIODevice
from loguru import logger

from models.db_tables import Task, TaskType
from utils.db_utils import get_session


class TaskListModel(QAbstractListModel):
    def __init__(self, task_type: TaskType, parent=None):
        super().__init__(parent)
        self.task_type = task_type
        self.tasks = []
        self.load_data()

    def load_data(self):
        with get_session(is_read_only=True) as session:
            self.tasks = [
                {
                    "id": task.id,
                    "task_name": task.task_name,
                    "task_position": task.task_position
                }
                for task in
                session.query(Task).filter(Task.task_type == self.task_type).order_by(Task.task_position).all()
            ]
        self.layoutChanged.emit()

    def index(self, row, column=0, parent=QModelIndex()):
        return self.createIndex(row, column)

    def data(self, index, role=...):
        if role == Qt.DisplayRole:
            return self.tasks[index.row()]["task_name"]
        return None

    def columnCount(self, parent):
        return 1

    def rowCount(self, parent=...):
        return len(self.tasks)

    def supportedDropActions(self):
        return Qt.DropAction.MoveAction

    def mimeData(self, indexes):
        mime_data = QMimeData()
        encoded_data = QByteArray()
        stream = QDataStream(encoded_data, QIODevice.WriteOnly)
        for index in indexes:
            if index.isValid():
                row = index.row()
                task_id = self.tasks[row]["id"]
                stream.writeInt32(row)
                stream.writeInt32(task_id)
                stream.writeQString(self.tasks[row]["task_name"])

        logger.debug(self.task_type)
        logger.debug(self.tasks)

        mime_data.setData("application/x-qabstractitemmodeldatalist", encoded_data)
        return mime_data

    def dropMimeData(self, data, action, row, column, parent):
        if not data.hasFormat("application/x-qabstractitemmodeldatalist"):
            return False

        encoded_data = data.data("application/x-qabstractitemmodeldatalist")
        stream = QDataStream(encoded_data, QIODevice.ReadOnly)
        new_tasks = []

        while not stream.atEnd():
            original_row = stream.readInt32()
            task_id = stream.readInt32()
            task_name = stream.readQString()
            new_tasks.append({"id": task_id, "task_name": task_name, "task_position": row})

        self.beginInsertRows(parent, row, row + len(new_tasks) - 1)
        for task in new_tasks:
            self.tasks.insert(row, task)
            row += 1
            self.layoutChanged.emit()
        self.endInsertRows()

        logger.debug(self.task_type)
        logger.debug(self.tasks)

        # Update task positions
        for i, task in enumerate(self.tasks):
            task["task_position"] = i

        self.layoutChanged.emit()
        return True


    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsDropEnabled

        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsDragEnabled | \
            Qt.ItemFlag.ItemIsDropEnabled | Qt.ItemFlag.ItemIsEnabled


    def mimeTypes(self):
        return ["application/x-qabstractitemmodeldatalist"]

    def insertRows(self, row, count, parent=None):
        self.beginInsertRows(parent, row, row + count - 1)
        encoded_data = self.mimeData([self.index(row)]).data("application/x-qabstractitemmodeldatalist")
        stream = QDataStream(encoded_data, QIODevice.ReadOnly)
        _row = stream.readInt32()
        task_id = stream.readInt32()
        task_name = stream.readQString()
        self.tasks.insert(row , {"id": task_id, "task_name": task_name, "task_position": row})
        self.layoutChanged.emit()
        self.endInsertRows()

    def removeRows(self, row, count, parent=...):
        self.beginRemoveRows(parent, row, row + count - 1)
        for i in range(count):
            del self.tasks[row]
        self.layoutChanged.emit()
        self.endRemoveRows()
        return True
