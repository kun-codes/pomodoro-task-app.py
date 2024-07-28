from sqlalchemy import URL, create_engine, Column, Integer, String, Enum as SQLEnum
from sqlalchemy.orm import declarative_base
from enum import Enum
from models.config import db_path

class TaskType(Enum):
    TODO = "todo"
    COMPLETED = "completed"

url_object = URL.create(
    'sqlite',
    database=db_path,
)

engine = create_engine(url_object)

Base = declarative_base()


class Task(Base):
    """
    Represents a table named "tasks" in the database
    """
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    task_name = Column(String)
    task_type = Column(SQLEnum(TaskType))


Base.metadata.create_all(engine)
