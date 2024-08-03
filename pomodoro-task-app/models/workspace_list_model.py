from PySide6.QtCore import Qt, QAbstractListModel
from sqlalchemy.orm import sessionmaker
from loguru import logger

from models.db_tables import Workspace, engine


class WorkspaceListModel(QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.workspaces = []
        self.load_data()
        self.layoutChanged.connect(self.logList)

    def load_data(self):
        session = sessionmaker(bind=engine)()
        self.workspaces = [
            {"id": workspace.id, "workspace_name": workspace.workspace_name}
            for workspace in session.query(Workspace).all()
        ]
        session.close()
        self.layoutChanged.emit()

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.workspaces[index.row()]["workspace_name"]
        if role == Qt.ItemDataRole.DisplayRole:
            return self.workspaces[index.row()]["id"]

    def rowCount(self, index):
        return len(self.workspaces)

    def add_workspace(self, workspace):
        session = sessionmaker(bind=engine)()
        session.add(workspace)
        session.commit()
        self.workspaces.append({"id": workspace.id, "workspace_name": workspace.workspace_name})
        session.close()
        self.layoutChanged.emit()

    # TODO: Implement update_workspace method

    def delete_workspace(self, index):
        if 0 <= index < len(self.workspaces):
            workspace_id = self.workspaces[index]["id"]
            session = sessionmaker(bind=engine)()
            workspace = session.get(Workspace, workspace_id)
            if workspace:
                session.delete(workspace)
                session.commit()
            session.close()
            self.workspaces.pop(index)
            self.layoutChanged.emit()

    def logList(self):
        logger.debug(f"Workspaces list in memory: {self.workspaces}")
