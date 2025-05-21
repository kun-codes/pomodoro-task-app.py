import signal
import sys
from pathlib import Path

from alembic import command
from alembic.config import Config
from PySide6.QtWidgets import QApplication

from main_window import MainWindow
from utils.check_valid_db import checkValidDB
from utils.is_nuitka import is_nuitka


def handle_signal(signal, frame):
    if mainWindow:
        # Properly cleanup the WebsiteBlockerManager
        mainWindow.website_blocker_manager.cleanup()
        mainWindow.website_blocker_manager.stop_filtering(delete_proxy=True)
    sys.exit(0)

# https://alembic.sqlalchemy.org/en/latest/cookbook.html#building-an-up-to-date-database-from-scratch
def run_alembic_upgrade():
    if is_nuitka():
        alembic_ini_path = Path("alembic.ini")
    else:
        alembic_ini_path = Path(__file__).parent.parent / "alembic.ini"
    alembic_cfg = Config(alembic_ini_path)
    # alembic_cfg.set_main_option("script_location", str(Path(__file__).parent.parent / "migrations"))
    command.upgrade(alembic_cfg, "head")


if __name__ == "__main__":
    run_alembic_upgrade()  # create db if it doesn't exist and run migrations
    checkValidDB()  # Check if the database is valid, if it doesn't have required sample data, add it

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    sys.exit(app.exec())
