from utils.db_utils import get_session
from models.db_tables import Task

class TaskLookup:
    @staticmethod
    def get_elapsed_time(task_id: int):
        with get_session(is_read_only=True) as session:
            task = session.get(Task, task_id)
        return task.elapsed_time if task else None

    @staticmethod
    def get_target_time(task_id: int):
        with get_session(is_read_only=True) as session:
            task = session.get(Task, task_id)
        return task.target_time if task else None
