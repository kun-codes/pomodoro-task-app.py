from sqlalchemy import URL, create_engine, Column, Integer, String, Enum as SQLEnum, Boolean, ForeignKey, event, Engine
from sqlalchemy.orm import declarative_base, relationship
from enum import Enum
from config_paths import db_path
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
    website_filter_type = Column(SQLEnum(WebsiteFilterType), default=WebsiteFilterType.BLOCKLIST)

    blocklist_urls = relationship("BlocklistURL", back_populates="workspace", cascade="all, delete-orphan")
    blocklist_exception_urls = relationship("BlocklistExceptionURL", back_populates="workspace", cascade="all, delete-orphan")
    allowlist_urls = relationship("AllowlistURL", back_populates="workspace", cascade="all, delete-orphan")
    allowlist_exception_urls = relationship("AllowlistExceptionURL", back_populates="workspace", cascade="all, delete-orphan")


class CurrentWorkspace(Base):
    """
    Represents a table named "current_workspace" in the database
    """
    __tablename__ = 'current_workspace'

    id = Column(Integer, primary_key=True)
    # TODO: use ` cascade="all, delete-orphan"` here too for more compatibility with other databases
    current_workspace_id = Column(Integer, ForeignKey('workspaces.id', ondelete='CASCADE'), unique=True, nullable=False)

class BlocklistURL(Base):
    __tablename__ = URLListType.BLOCKLIST.value
    id = Column(Integer, primary_key=True)
    workspace_id = Column(Integer, ForeignKey('workspaces.id'))
    url = Column(String, nullable=False)

    workspace = relationship("Workspace", back_populates="blocklist_urls")

class BlocklistExceptionURL(Base):
    __tablename__ = URLListType.BLOCKLIST_EXCEPTION.value
    id = Column(Integer, primary_key=True)
    workspace_id = Column(Integer, ForeignKey('workspaces.id'))
    url = Column(String, nullable=False)

    workspace = relationship("Workspace", back_populates="blocklist_exception_urls")

class AllowlistURL(Base):
    __tablename__ = URLListType.ALLOWLIST.value
    id = Column(Integer, primary_key=True)
    workspace_id = Column(Integer, ForeignKey('workspaces.id'))
    url = Column(String, nullable=False)

    workspace = relationship("Workspace", back_populates="allowlist_urls")

class AllowlistExceptionURL(Base):
    __tablename__ = URLListType.ALLOWLIST_EXCEPTION.value
    id = Column(Integer, primary_key=True)
    workspace_id = Column(Integer, ForeignKey('workspaces.id'))
    url = Column(String, nullable=False)

    workspace = relationship("Workspace", back_populates="allowlist_exception_urls")


Base.metadata.create_all(engine)
