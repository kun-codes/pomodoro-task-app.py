from PySide6.QtCore import Qt, QAbstractListModel, QItemSelectionModel, Signal, QModelIndex
from sqlalchemy.orm import sessionmaker
from loguru import logger

from models.db_tables import Workspace, engine, CurrentWorkspace


class WorkspaceListModel(QAbstractListModel):
    current_workspace_changed = Signal()
    current_workspace_deleted = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.workspaces = []
        self.load_data()
        self.layoutChanged.connect(self.logList)
        self.selection_model: QItemSelectionModel = None

    def setSelectionModel(self, selection_model: QItemSelectionModel):
        self.selection_model = selection_model

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

    def rowCount(self, index=QModelIndex()):
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
            workspace_id = self.workspaces[index]["id"]  # workspace about to be deleted
            selected_workspace_id = self.get_current_workspace_id()
            session = sessionmaker(bind=engine)()
            workspace = session.get(Workspace, workspace_id)
            if workspace:
                session.delete(workspace)
                session.commit()
                if workspace_id == selected_workspace_id:
                    self.current_workspace_deleted.emit()
            session.close()
            self.workspaces.pop(index)
            self.layoutChanged.emit()

    def set_current_workspace_preference(self):
        if self.selection_model:
            selected_index = self.selection_model.currentIndex()
            if selected_index.isValid():
                selected_workspace = self.workspaces[selected_index.row()]
                session = sessionmaker(bind=engine)()

                previous_selected_workspace = session.query(CurrentWorkspace).first()
                previous_selected_workspace_id = previous_selected_workspace.current_workspace_id \
                    if previous_selected_workspace else None
                # make sure that only one record exists in current_workspace table
                session.query(CurrentWorkspace).delete()
                current_workspace = CurrentWorkspace(current_workspace_id=selected_workspace["id"])
                session.add(current_workspace)
                session.commit()
                session.close()

                self.load_data()

                current_workspace_id = session.query(CurrentWorkspace).first().current_workspace_id

                if previous_selected_workspace_id != current_workspace_id:
                    self.current_workspace_changed.emit()

    def get_current_workspace_id(self):
        session = sessionmaker(bind=engine)()
        current_workspace = session.query(CurrentWorkspace).first()
        session.close()
        return current_workspace.current_workspace_id if current_workspace else None

    def get_workspace_name_by_id(self, workspace_id):
        for workspace in self.workspaces:
            if workspace["id"] == workspace_id:
                return workspace["workspace_name"]
        return None

    def logList(self):
        logger.debug(f"Workspaces list in memory: {self.workspaces}")


workspace_list_model = WorkspaceListModel()