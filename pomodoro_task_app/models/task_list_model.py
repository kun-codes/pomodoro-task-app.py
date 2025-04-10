from loguru import logger
from PySide6.QtCore import QAbstractListModel, QByteArray, QDataStream, QIODevice, QMimeData, QModelIndex, Qt, Signal
from PySide6.QtGui import QColor
from qfluentwidgets import FluentIcon
from sqlalchemy import update

from models.config import AppSettings
from models.db_tables import Task, TaskType
from models.workspace_lookup import WorkspaceLookup
from utils.db_utils import get_session


class TaskListModel(QAbstractListModel):
    IDRole = Qt.UserRole + 1
    IconRole = Qt.UserRole + 3
    ElapsedTimeRole = Qt.UserRole + 5
    TargetTimeRole = Qt.UserRole + 7

    taskDeletedSignal = Signal(int)  # task_id
    taskMovedSignal = Signal(int, TaskType)  # task_id and TaskType
    currentTaskChangedSignal = Signal(int)  # task_id

    def __init__(self, task_type: TaskType, parent=None):
        super().__init__(parent)
        self.task_type = task_type
        self.current_task_id = None
        self.tasks = []
        self.load_data()

    def setCurrentTaskID(self, id):
        self.current_task_id = id
        self.currentTaskChangedSignal.emit(id)

    def currentTaskID(self):
        return self.current_task_id

    def load_data(self):
        current_workspace_id = WorkspaceLookup.get_current_workspace_id()
        self.tasks = []
        with get_session(is_read_only=True) as session:
            self.tasks = [
                {
                    "id": task.id,
                    "task_name": task.task_name,
                    "task_position": task.task_position,
                    "elapsed_time": task.elapsed_time,  # in ms
                    "target_time": task.target_time,  # in ms
                    "icon": FluentIcon.PLAY if self.task_type == TaskType.TODO else FluentIcon.MENU,
                }
                for task in session.query(Task)
                .filter(Task.task_type == self.task_type)
                .filter(Task.workspace_id == current_workspace_id)
                .order_by(Task.task_position)
                .all()
            ]
        self.layoutChanged.emit()

    def index(self, row, column=0, parent=QModelIndex()):
        return self.createIndex(row, column)

    def data(self, index, role=...):
        if role == Qt.DisplayRole:
            return self.tasks[index.row()]["task_name"]
        elif role == self.ElapsedTimeRole:
            task = self.tasks[index.row()]
            return task["elapsed_time"]
        elif role == self.TargetTimeRole:
            task = self.tasks[index.row()]
            return task["target_time"]
        elif role == self.IDRole:
            task = self.tasks[index.row()]
            return task["id"]
        elif role == self.IconRole:
            task = self.tasks[index.row()]
            return task["icon"]
        elif role == Qt.ItemDataRole.BackgroundRole:
            if self.current_task_id == self.tasks[index.row()]["id"]:
                theme_color: QColor = AppSettings.get(AppSettings, AppSettings.themeColor)
                return theme_color  # use theme color to color current task
            else:
                return None  # use default color according to dark/light theme

        return None

    def setData(self, index, value, role=..., update_db=True):
        if role == Qt.DisplayRole:
            row = index.row()
            task_name = value.strip()
            if task_name:
                self.tasks[row]["task_name"] = task_name
                self.update_db()
                self.dataChanged.emit(index, index)
                return True
        elif role == self.ElapsedTimeRole:
            row = index.row()
            elapsed_time = value
            self.tasks[row]["elapsed_time"] = elapsed_time
            if update_db:
                self.update_db()
            self.dataChanged.emit(index, index)
            return True
        elif role == self.TargetTimeRole:
            row = index.row()
            target_time = value
            self.tasks[row]["target_time"] = target_time
            self.update_db()
            self.dataChanged.emit(index, index)
            return True
        elif role == self.IconRole:
            row = index.row()
            icon = value
            self.tasks[row]["icon"] = icon
            self.dataChanged.emit(index, index)
            return True
        return False

    def revert(self):
        self.load_data()
        return super().revert()

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
                stream.writeInt64(self.tasks[row]["elapsed_time"])
                stream.writeInt64(self.tasks[row]["target_time"])

        # update task positions
        rows_to_be_remove = []
        for index in indexes:
            if index.isValid():
                row = index.row()
                rows_to_be_remove.append(row)

        removed_rows_count = 0
        for i, task in enumerate(self.tasks):
            if i in rows_to_be_remove:
                task["task_position"] = -1  # setting task position to -1 to indicate that it will be removed
                removed_rows_count += 1
            else:
                task["task_position"] = i - removed_rows_count  # subtracting removed rows count from current index
                # so that numbers skipped for removed rows are accounted for
        self.update_db()

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
            original_row = stream.readInt32()  # noqa: F841
            task_id = stream.readInt32()
            task_name = stream.readQString()
            elapsed_time = stream.readInt64()
            target_time = stream.readInt64()
            new_tasks.append(
                {
                    "id": task_id,
                    "task_name": task_name,
                    "task_position": row,
                    "elapsed_time": elapsed_time,
                    "target_time": target_time,
                    "icon": FluentIcon.PLAY if self.task_type == TaskType.TODO else FluentIcon.MENU,
                }
            )

        self.beginInsertRows(parent, row, row + len(new_tasks) - 1)
        for task in new_tasks:
            self.tasks.insert(row, task)
            row += 1
            self.taskMovedSignal.emit(task["id"], self.task_type)
        self.endInsertRows()

        # Update task positions
        for i, task in enumerate(self.tasks):
            task["task_position"] = i

        self.update_db()

        logger.debug(self.task_type)
        logger.debug(self.tasks)

        self.layoutChanged.emit()
        return True

    def update_db(self):
        """
        updating db, using bulk insert
        https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-update
        """
        current_workspace_id = WorkspaceLookup.get_current_workspace_id()
        with get_session() as session:
            session.execute(
                update(Task),
                [
                    {
                        "id": task["id"],
                        "workspace_id": current_workspace_id,
                        "task_name": task["task_name"],
                        "task_type": self.task_type,
                        "task_position": task["task_position"],
                        "elapsed_time": task["elapsed_time"],
                        "target_time": task["target_time"],
                    }
                    for task in self.tasks
                ],
            )

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsDropEnabled

        return (
            Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsSelectable
            | Qt.ItemFlag.ItemIsDragEnabled
            | Qt.ItemFlag.ItemIsDropEnabled
            | Qt.ItemFlag.ItemIsEditable
        )

    def mimeTypes(self):
        return ["application/x-qabstractitemmodeldatalist"]

    # TODO: Implement insertRows method
    # def insertRows(self, row, count, parent=None):
    #     self.beginInsertRows(parent, row, row + count - 1)
    #     encoded_data = self.mimeData([self.index(row)]).data("application/x-qabstractitemmodeldatalist")
    #     stream = QDataStream(encoded_data, QIODevice.ReadOnly)
    #     _row = stream.readInt32()
    #     task_id = stream.readInt32()
    #     task_name = stream.readQString()
    #     return True

    def insertRow(self, row, parent=QModelIndex(), task_name=None, task_type=TaskType.TODO):
        """
        Used to insert a new task in the list
        """
        self.beginInsertRows(parent, row, row)

        with get_session() as session:
            task = Task(
                workspace_id=WorkspaceLookup.get_current_workspace_id(),
                task_name=task_name,
                task_type=task_type,
                task_position=row,
            )
            session.add(task)
            session.commit()
            new_id = task.id

        task_list_new_member = {
            "id": new_id,
            "task_name": task_name,
            "task_position": row,
            "elapsed_time": 0,
            "target_time": 0,
            "icon": FluentIcon.PLAY if self.task_type == TaskType.TODO else FluentIcon.MENU,
        }

        logger.debug(f"Task list new member: {task_list_new_member}")

        self.tasks.insert(row, task_list_new_member)
        self.endInsertRows()
        self.layoutChanged.emit()
        return True

    def removeRows(self, row, count, parent=...):
        """
        remove rows but not delete from db
        """
        self.beginRemoveRows(parent, row, row + count - 1)
        for i in range(count):
            logger.debug(f"tasks: {self.tasks}")
            logger.debug(f"Removing task at row: {row}")
            del self.tasks[row]
            logger.debug(f"tasks: {self.tasks}")
        self.endRemoveRows()

        # Update task positions
        for i, task in enumerate(self.tasks):
            task["task_position"] = i

        self.layoutChanged.emit()
        return True

    def deleteTask(self, row, parent=QModelIndex()):
        """
        will remove rows as well as delete from database
        """
        logger.debug(f"Deleting task at row: {row}")
        task_id = self.tasks[row]["id"]
        # get index of row
        with get_session() as session:
            task = session.query(Task).get(task_id)
            session.delete(task)

        logger.debug(f"tasks: {self.tasks}")
        self.removeRows(row, 1, parent)

        for i, task in enumerate(self.tasks):
            task["task_position"] = i

        self.update_db()
        self.taskDeletedSignal.emit(task_id)
        self.layoutChanged.emit()
        return True

    def setIconForTask(self, row, icon):
        self.tasks[row]["icon"] = icon
        self.dataChanged.emit(self.index(row, 0), self.index(row, 0), [self.IconRole])

    def getTaskNameById(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                return task["task_name"]
        return None

    def currentTaskIndex(self):
        for task in self.tasks:
            if task["id"] == self.current_task_id:
                return self.index(task["task_position"], 0)
