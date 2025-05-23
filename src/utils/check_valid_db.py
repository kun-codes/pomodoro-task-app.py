from models.db_tables import CurrentWorkspace, Task, TaskType, Version, Workspace
from utils.db_utils import get_session
from utils.get_app_version import get_app_version


def checkValidDB():
    with get_session() as session:
        # Initialize version info if not exists
        # todo: make a upgrade db function too for future app versions
        if not session.query(Version).first():
            version = Version(app_version=get_app_version())
            session.add(version)
            session.commit()

        workspace = session.query(Workspace).first()
        # create a default workspace if none exists
        if not workspace:
            workspace = Workspace(workspace_name="Default Workspace")
            session.add(workspace)
            session.commit()

            # add some tasks too
            sample_tasks = [
                Task(workspace_id=workspace.id, task_name="Sample Task 1", task_type=TaskType.TODO, task_position=0),
                Task(workspace_id=workspace.id, task_name="Sample Task 2", task_type=TaskType.TODO, task_position=1),
                Task(workspace_id=workspace.id, task_name="Sample Task 3", task_type=TaskType.TODO, task_position=2),
                Task(
                    workspace_id=workspace.id,
                    task_name="Sample Task 4",
                    task_type=TaskType.COMPLETED,
                    task_position=3,
                ),
                Task(
                    workspace_id=workspace.id,
                    task_name="Sample Task 5",
                    task_type=TaskType.COMPLETED,
                    task_position=4,
                ),
                Task(
                    workspace_id=workspace.id,
                    task_name="Sample Task 6",
                    task_type=TaskType.COMPLETED,
                    task_position=5,
                ),
            ]
            session.add_all(sample_tasks)
            session.commit()

        # if application was closed while no workspace was selected, select the first workspace in the database
        # if database had no workspace to begin with then set default workspace as current database
        current_workspace = session.query(CurrentWorkspace).first()
        if not current_workspace:
            current_workspace = CurrentWorkspace(current_workspace_id=workspace.id)
            session.add(current_workspace)
            session.commit()
