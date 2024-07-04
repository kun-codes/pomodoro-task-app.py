import sys
from enum import Enum
from PySide6.QtCore import QTimer, Signal, QObject
from PySide6.QtWidgets import QApplication
from loguru import logger

from constants import BREAK_DURATION, WORK_DURATION, LONG_BREAK_DURATION, WORK_INTERVALS

# Enum which tells what state the timer is in
class TimerState(Enum):
    NOTHING = 1
    WORK = 2
    BREAK = 3
    LONG_BREAK = 4


class PomodoroTimer(QObject):
    def __init__(self):
        super().__init__()
        self.timer_state = TimerState.NOTHING
        self.pomodoro_timer = QTimer()
        self.session_progress = 0  # would be incremented by 0.5 after every work ended signal is emitted
        # would also be incremented by 0.5 after every break ended signal is emitted
        # starts out at 0 which means that the timer state is NOTHING
        # whole number means that break is going on
        # would be reset to zero after every long break

        self.pomodoro_timer.timeout.connect(self.sessionEnded)

    def getTimerState(self):
        return self.timer_state

    def updateSessionProgress(self):
        logger.debug(f"Session Progress (before): {self.session_progress}")
        logger.debug(f"Timer State (before): {self.timer_state}")
        if self.timer_state == TimerState.WORK:
            if self.session_progress < WORK_INTERVALS - 0.5:
                self.session_progress += 0.5
            elif self.session_progress == WORK_INTERVALS - 0.5:
                self.session_progress = 0
        elif self.timer_state == TimerState.BREAK:
            self.session_progress += 0.5
        elif self.timer_state == TimerState.NOTHING:
            self.session_progress += 0.5

    def startSession(self):
        if self.getTimerState() == TimerState.NOTHING:
            self.updateSessionProgress()
            self.timer_state = TimerState.WORK
            self.pomodoro_timer.start(WORK_DURATION * 60 * 1000)
            logger.debug("***Starting work session after nothing state")
        elif self.getTimerState() == TimerState.WORK and self.session_progress < WORK_INTERVALS - 0.5:
            self.updateSessionProgress()
            self.timer_state = TimerState.BREAK
            self.pomodoro_timer.start(BREAK_DURATION * 60 * 1000)
            logger.debug("***Starting break session")
        elif self.getTimerState() == TimerState.WORK and self.session_progress == WORK_INTERVALS - 0.5:
            self.updateSessionProgress()
            self.timer_state = TimerState.LONG_BREAK
            self.pomodoro_timer.start(LONG_BREAK_DURATION * 60 * 1000)
            logger.debug("***Starting long break session")
        elif self.getTimerState() == TimerState.BREAK:
            self.updateSessionProgress()
            self.timer_state = TimerState.WORK
            self.pomodoro_timer.start(WORK_DURATION * 60 * 1000)
            logger.debug("***Starting work session after break")

        logger.debug(f"Session Progress (after): {self.session_progress}")
        logger.debug(f"Timer State (after): {self.timer_state}")

    def sessionEnded(self):
        if self.timer_state == TimerState.WORK and self.session_progress < WORK_INTERVALS - 0.5:
            self.startSession()  # Start the break
        elif self.timer_state == TimerState.WORK and self.session_progress == WORK_INTERVALS - 0.5:
            self.startSession()  # Start the long break
        elif self.timer_state == TimerState.BREAK:
            self.startSession()  # Start the work session
        elif self.timer_state == TimerState.LONG_BREAK:
            self.pomodoroSessionEnded()

        logger.debug(f"Remaining time: {self.timer_duration/1000}")
    def pomodoroSessionEnded(self):
        logger.debug("Pomodoro Session Ended")
        self.pomodoro_timer.stop()
        self.timer_state = TimerState.NOTHING


if __name__ == '__main__':
    class TestPomodoro:
        def __init__(self):
            self.pomodoro_timer = PomodoroTimer()

            self.pomodoro_timer.startSession()


    app = QApplication(sys.argv)
    pomodoro_test = TestPomodoro()
    app.exec()
