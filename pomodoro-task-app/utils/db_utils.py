from contextlib import contextmanager

from models.db_tables import engine
from sqlalchemy.orm import sessionmaker


@contextmanager
def get_session(is_read_only=False):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
        if not is_read_only:
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
