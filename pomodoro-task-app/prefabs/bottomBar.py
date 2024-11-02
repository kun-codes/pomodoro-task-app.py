from PySide6.QtWidgets import QWidget
from qfluentwidgets import FluentIcon

from ui_py.ui_bottom_bar_widget import Ui_BottomBarWidget

class BottomBar(Ui_BottomBarWidget, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=None)
        self.setupUi(self)

        self.initWidget()

    def initWidget(self):
        self.pauseResumeButton.setIcon(FluentIcon.PLAY)
        self.skipButton.setIcon(FluentIcon.CHEVRON_RIGHT)

        self.pauseResumeButton.setCheckable(True)
        self.pauseResumeButton.setChecked(True)
        self.skipButton.setCheckable(False)

        print(self.timerLabel)
        print(self.taskLabel)