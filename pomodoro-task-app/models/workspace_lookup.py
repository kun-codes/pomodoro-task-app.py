from utils.db_utils import get_session
from models.db_tables import CurrentWorkspace, Workspace

class WorkspaceLookup:
    @staticmethod
    def get_current_workspace_id():
        with get_session(is_read_only=True) as session:
            current_workspace = session.query(CurrentWorkspace).first()
        return current_workspace.current_workspace_id if current_workspace else None

    @staticmethod
    def get_current_workspace_name():
        current_workspace_id = WorkspaceLookup.get_current_workspace_id()
        with get_session(is_read_only=True) as session:
            workspace = session.get(Workspace, current_workspace_id)
        return workspace.workspace_name if workspace else None

    @staticmethod
    def get_current_workspace():
        current_workspace_id = WorkspaceLookup.get_current_workspace_id()
        with get_session(is_read_only=True) as session:
            workspace = session.get(Workspace, current_workspace_id)
        return workspace

if __name__ == '__main__':
    print(WorkspaceLookup.get_current_workspace_id())
    print(WorkspaceLookup.get_current_workspace_name())
