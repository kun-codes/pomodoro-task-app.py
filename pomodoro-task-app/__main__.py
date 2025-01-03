import signal
import sys

from main_window import MainWindow
from PySide6.QtWidgets import QApplication


def handle_signal(signal, frame):
    if mainWindow:
        mainWindow.website_blocker_manager.stop_filtering(delete_proxy=True)
    sys.exit(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    sys.exit(app.exec())
