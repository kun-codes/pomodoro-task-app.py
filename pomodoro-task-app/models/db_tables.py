from sqlalchemy import URL, create_engine, Column, Integer, String, Enum as SQLEnum, Boolean, ForeignKey, event, Engine
from sqlalchemy.orm import declarative_base
from enum import Enum
from models.config import db_path
from constants import WORK_DURATION, BREAK_DURATION, LONG_BREAK_DURATION, WORK_INTERVALS, AUTOSTART_WORK, \
    AUTOSTART_BREAK
from constants import WebsiteFilterType, URLListType

url_object = URL.create(
    'sqlite',
    database=db_path,
)
engine = create_engine(url_object)
Base = declarative_base()

# from: https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#foreign-key-support
# for supporting foreign keys in sqlite as they are disabled by default as per: https://www.sqlite.org/foreignkeys.html
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

class TaskType(Enum):
    TODO = "todo"
    COMPLETED = "completed"


class Task(Base):
    """
    Represents a table named "tasks" in the database
    """
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    task_name = Column(String)
    task_type = Column(SQLEnum(TaskType))
    task_position = Column(Integer)

class Workspace(Base):
    """
    Represents a table named "workspaces" in the database
    """
    __tablename__ = 'workspaces'

    id = Column(Integer, primary_key=True)
    workspace_name = Column(String, nullable=False)
    work_duration = Column(Integer, default=WORK_DURATION)
    break_duration = Column(Integer, default=BREAK_DURATION)
    long_break_duration = Column(Integer, default=LONG_BREAK_DURATION)
    work_intervals = Column(Integer, default=WORK_INTERVALS)
    autostart_work = Column(Boolean, default=AUTOSTART_WORK)
    autostart_break = Column(Boolean, default=AUTOSTART_BREAK)

class CurrentWorkspace(Base):
    """
    Represents a table named "current_workspace" in the database
    """
    __tablename__ = 'current_workspace'

    id = Column(Integer, primary_key=True)
    current_workspace_id = Column(Integer, ForeignKey('workspaces.id', ondelete='CASCADE'), unique=True, nullable=False)


Base.metadata.create_all(engine)
