from loguru import logger
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
        self.pomodoro_timer_obj.timerStateChangedSignal.connect(self.initProgressRing)

    def editButtonProperties(self):
        self.restartButton.setIcon(FluentIcon.UPDATE)
        self.pauseResumeButton.setIcon(FluentIcon.PAUSE)
        self.skipButton.setIcon(FluentIcon.CHEVRON_RIGHT)

        self.restartButton.setCheckable(False)
        self.pauseResumeButton.setCheckable(False)
        self.skipButton.setCheckable(False)

    def stopButtonClicked(self):
        logger.debug("Restart Button Clicked")
        self.pomodoro_timer_obj.stopSession()
        self.pauseResumeButton.setChecked(True)
        self.pauseResumeButton.setIcon(FluentIcon.PLAY)

    def pauseResumeButtonClicked(self):
        if self.pauseResumeButton.isChecked():
            self.pauseResumeButton.setIcon(FluentIcon.PLAY)
            self.pomodoro_timer_obj.pauseDuration()
        else:
            self.pauseResumeButton.setIcon(FluentIcon.PAUSE)
            self.pomodoro_timer_obj.startDuration()

    def initProgressRing(self, currentTimerState: TimerState):
        logger.debug("Init Progress Ring")
        self.ProgressRing.setMinimum(0)

        if currentTimerState == TimerState.WORK:
            self.ProgressRing.setMaximum(WORK_DURATION * 60 * 1000)
        elif currentTimerState == TimerState.BREAK:
            self.ProgressRing.setMaximum(BREAK_DURATION * 60 * 1000)
        elif currentTimerState == TimerState.LONG_BREAK:
            self.ProgressRing.setMaximum(LONG_BREAK_DURATION * 60 * 1000)
        elif currentTimerState == TimerState.NOTHING:
            self.ProgressRing.setMaximum(0)

        self.ProgressRing.setValue(self.ProgressRing.maximum())

    def updateProgressRing(self):
        self.ProgressRing.setValue(self.ProgressRing.value() - 1000)

    def skipButtonClicked(self):
        # TODO: Implement skip button functionality
        logger.info("Skip Button Clicked")
        # self.pomodoro_timer.skipDuration()




if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = PomodoroView()
    window.show()
    sys.exit(app.exec_())