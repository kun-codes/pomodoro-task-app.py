from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QSpacerItem, QSizePolicy, QHBoxLayout

from qfluentwidgets import FluentIcon, PillPushButton

from ui_py.ui_pomodoro_view import Ui_PomodoroView

class HorizontalSpacer(QSpacerItem):
    def __init__(self):
        super().__init__(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

class PomodoroView(QWidget, Ui_PomodoroView):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.editButtonProperties()

        self.restartButton.clicked.connect(self.restartButtonClicked)

        # self.pauseResumeButton.setIcon(FluentIcon.PAUSE)
        # self.skipButton.setIcon(FluentIcon.CHEVRON_RIGHT)
        # self.restartButton.setIcon(FluentIcon.UPDATE)

    def editButtonProperties(self):
        self.restartButton.setIcon(FluentIcon.UPDATE)
        self.pauseResumeButton.setIcon(FluentIcon.PAUSE)
        self.skipButton.setIcon(FluentIcon.CHEVRON_RIGHT)

        self.restartButton.setCheckable(False)
        self.pauseResumeButton.setCheckable(False)
        self.skipButton.setCheckable(False)


    def restartButtonClicked(self):
        print("Restart Button Clicked")



if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = PomodoroView()
    window.show()
    sys.exit(app.exec_())