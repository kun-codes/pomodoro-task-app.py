from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QSpacerItem, QSizePolicy
from loguru import logger
from qfluentwidgets import FluentIcon

from config_values import ConfigValues
from models.timer import PomodoroTimer, TimerState
from ui_py.ui_pomodoro_view import Ui_PomodoroView


class HorizontalSpacer(QSpacerItem):
    def __init__(self):
        super().__init__(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)


class PomodoroView(QWidget, Ui_PomodoroView):
    """
    For pomodoro view of the app
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.initButtonProperties()

        self.stopButton.clicked.connect(self.stopButtonClicked)
        self.pauseResumeButton.clicked.connect(self.pauseResumeButtonClicked)
        self.skipButton.clicked.connect(self.skipButtonClicked)

        self.pomodoro_timer_obj = PomodoroTimer()
        self.pomodoro_timer_obj.timerStateChangedSignal.connect(self.initProgressRing)
        self.pomodoro_timer_obj.pomodoro_timer.timeout.connect(self.updateProgressRing)
        self.pomodoro_timer_obj.sessionEndedSignal.connect(self.resetPauseResumeButton)
        self.pomodoro_timer_obj.waitForUserInputSignal.connect(self.resetPauseResumeButton)

        self.initProgressRingProperties()

    def initProgressRingProperties(self):
        self.ProgressRing.setTextVisible(True)
        progress_ring_label_font = QFont()
        # progress_ring_label_font.setFamilies([u"Microsoft YaHei UI"])
        progress_ring_label_font.setPointSize(14)
        progress_ring_label_font.setBold(False)
        self.ProgressRing.setFont(progress_ring_label_font)
        self.ProgressRing.setFormat(self.pomodoro_timer_obj.getTimerState().value)

    def initButtonProperties(self):
        self.stopButton.setIcon(FluentIcon.CLOSE)
        self.pauseResumeButton.setIcon(FluentIcon.PLAY)
        self.skipButton.setIcon(FluentIcon.CHEVRON_RIGHT)

        self.stopButton.setCheckable(False)
        self.pauseResumeButton.setCheckable(True)
        self.pauseResumeButton.setChecked(True)
        self.skipButton.setCheckable(False)

    def stopButtonClicked(self):
        logger.debug("Stop Button Clicked")
        self.pomodoro_timer_obj.stopSession()

    def pauseResumeButtonClicked(self):
        if self.pauseResumeButton.isChecked():
            self.pauseResumeButton.setIcon(FluentIcon.PLAY)
            self.pomodoro_timer_obj.pauseDuration()
        else:
            self.pauseResumeButton.setIcon(FluentIcon.PAUSE)
            if self.pomodoro_timer_obj.getTimerState() == TimerState.NOTHING:
                self.pomodoro_timer_obj.updateSessionProgress()
            self.pomodoro_timer_obj.setDuration()
            self.pomodoro_timer_obj.startDuration()

    def initProgressRing(self, currentTimerState: TimerState):
        self.ProgressRing.setMinimum(0)

        if currentTimerState == TimerState.WORK:
            self.ProgressRing.setMaximum(ConfigValues.WORK_DURATION * 60 * 1000)
        elif currentTimerState == TimerState.BREAK:
            self.ProgressRing.setMaximum(ConfigValues.BREAK_DURATION * 60 * 1000)
        elif currentTimerState == TimerState.LONG_BREAK:
            self.ProgressRing.setMaximum(ConfigValues.LONG_BREAK_DURATION * 60 * 1000)
        elif currentTimerState == TimerState.NOTHING:
            self.ProgressRing.reset()

        if self.pomodoro_timer_obj.getTimerState() != TimerState.NOTHING:
            self.ProgressRing.setValue(self.ProgressRing.maximum())
        else:
            self.ProgressRing.setValue(0)

        # display current timer state value along with the full duration formatted to clock format
        hours, minutes, seconds = self.convert_milliseconds(self.ProgressRing.maximum())
        if self.pomodoro_timer_obj.getTimerState() != TimerState.NOTHING:
            if hours != 0:
                self.ProgressRing.setFormat(f"{currentTimerState.value}\n{hours:02d}:{minutes:02d}:{seconds:02d}")
            else:
                self.ProgressRing.setFormat(f"{currentTimerState.value}\n{minutes:02d}:{seconds:02d}")
        else:
            self.ProgressRing.setFormat(self.pomodoro_timer_obj.getTimerState().value)

    def updateProgressRing(self):
        if self.pomodoro_timer_obj.getTimerState() != TimerState.NOTHING:
            hours, minutes, seconds = self.convert_milliseconds(self.pomodoro_timer_obj.getRemainingTime())
            currentTimerState = self.pomodoro_timer_obj.getTimerState().value
            if hours != 0:
                self.ProgressRing.setFormat(f"{currentTimerState}\n{hours:02d}:{minutes:02d}:{seconds:02d}")
            else:
                self.ProgressRing.setFormat(f"{currentTimerState}\n{minutes:02d}:{seconds:02d}")

        self.ProgressRing.setValue(self.pomodoro_timer_obj.getRemainingTime())

    def skipButtonClicked(self):
        self.pomodoro_timer_obj.skipDuration()

    def resetPauseResumeButton(self):
        self.pauseResumeButton.setChecked(True)
        self.pauseResumeButton.setIcon(FluentIcon.PLAY)

    def convert_milliseconds(self, milliseconds):
        seconds, milliseconds = divmod(milliseconds, 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return int(hours), int(minutes), int(seconds)


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = PomodoroView()
    window.show()
    sys.exit(app.exec())
