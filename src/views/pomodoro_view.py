from loguru import logger

from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QSpacerItem, QSizePolicy, QHBoxLayout
from qfluentwidgets import FluentIcon, PillPushButton

from ui_py.ui_pomodoro_view import Ui_PomodoroView
from models.timer import PomodoroTimer, TimerState
from constants import WORK_DURATION, BREAK_DURATION, LONG_BREAK_DURATION, WORK_INTERVALS


class HorizontalSpacer(QSpacerItem):
    def __init__(self):
        super().__init__(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)


class PomodoroView(QWidget, Ui_PomodoroView):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.initButtonProperties()
        self.initProgressRingProperties()


        self.stopButton.clicked.connect(self.stopButtonClicked)
        self.pauseResumeButton.clicked.connect(self.pauseResumeButtonClicked)
        self.skipButton.clicked.connect(self.skipButtonClicked)

        self.pomodoro_timer_obj = PomodoroTimer()
        self.pomodoro_timer_obj.timerStateChangedSignal.connect(self.initProgressRing)
        self.pomodoro_timer_obj.pomodoro_timer.timeout.connect(self.updateProgressRing)

    def initProgressRingProperties(self):
        self.ProgressRing.setTextVisible(True)
        progress_ring_label_font = QFont()
        # progress_ring_label_font.setFamilies([u"Microsoft YaHei UI"])
        # TODO: make progress ring label font same as the one used in labels
        progress_ring_label_font.setPointSize(14)
        progress_ring_label_font.setBold(False)
        self.ProgressRing.setFont(progress_ring_label_font)
        self.ProgressRing.setFormat("Formatted Text")


    def initButtonProperties(self):
        self.stopButton.setIcon(FluentIcon.CLOSE)
        self.pauseResumeButton.setIcon(FluentIcon.PLAY)
        self.skipButton.setIcon(FluentIcon.CHEVRON_RIGHT)

        self.stopButton.setCheckable(False)
        self.pauseResumeButton.setCheckable(True)
        self.pauseResumeButton.setChecked(True)
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
    sys.exit(app.exec())
