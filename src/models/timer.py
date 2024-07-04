import sys
from enum import Enum

from PySide6.QtCore import QTimer, Signal, QObject
from PySide6.QtWidgets import QApplication
from loguru import logger

from constants import BREAK_DURATION, WORK_DURATION, LONG_BREAK_DURATION, WORK_INTERVALS

# Enum which tells what state the timer is in
class TimerState(Enum):
    NOTHING = "Begin Timer"
    WORK = "Work"
    BREAK = "Break"
    LONG_BREAK = "Long Break"


class PomodoroTimer(QObject):  # Inherit from QObject to support signals
    # first argument for current timer state
    timerStateChangedSignal = Signal(TimerState)

    def __init__(self):
        super().__init__()
        self.timer_state = TimerState.NOTHING
        self.pomodoro_timer = QTimer()
        self.session_progress = 0  # would be incremented by 0.5 after every work ended signal is emitted
        # would also be incremented by 0.5 after every break ended signal is emitted
        # starts out at 0 which means that the timer state is NOTHING
        # whole number means that break is going on
        # would be reset to zero after every long break

        self.timer_duration = 0  # will change according to BREAK_DURATION, WORK_DURATION, LONG_BREAK_DURATION

        # self.pomodoro_timer.timeout.connect(self.sessionEnded)
        self.pomodoro_timer.timeout.connect(self.decreaseRemainingTime)

    def getTimerState(self):
        return self.timer_state

    # increments the session tracking variable session_progress by 0.5 or resets to 0 depending on the timer state
    def updateSessionProgress(self):
        logger.debug(f"Session Progress (before): {self.session_progress}")
        logger.debug(f"Timer State (before): {self.timer_state}")

        if self.timer_state == TimerState.WORK:
            if self.session_progress < WORK_INTERVALS - 0.5:
                self.session_progress += 0.5
            elif self.session_progress == WORK_INTERVALS - 0.5:
                self.session_progress += 0.5
        elif self.timer_state == TimerState.BREAK:
            self.session_progress += 0.5
        elif self.timer_state == TimerState.NOTHING:
            self.session_progress += 0.5

    # starts the timer for the work session, break session or long break session
    def startDuration(self):
        if self.timer_duration > 0 and not self.pomodoro_timer.isActive():
            logger.info("Resuming timer")
            self.pomodoro_timer.start(1000)
        else:
            if self.getTimerState() == TimerState.NOTHING:
                self.updateSessionProgress()
                self.timer_state = TimerState.WORK
                logger.info("Starting work session after nothing state")
                self.setTimerDuration(WORK_DURATION * 60 * 1000)
                self.pomodoro_timer.start(1000)

            elif self.getTimerState() == TimerState.WORK and self.session_progress < WORK_INTERVALS - 0.5:
                self.updateSessionProgress()
                self.setTimerDuration(BREAK_DURATION * 60 * 1000)
                self.timer_state = TimerState.BREAK
                logger.info("Starting break session")
                self.pomodoro_timer.start(1000)

            elif self.getTimerState() == TimerState.WORK and self.session_progress == WORK_INTERVALS - 0.5:
                self.updateSessionProgress()
                self.setTimerDuration(LONG_BREAK_DURATION * 60 * 1000)
                self.timer_state = TimerState.LONG_BREAK
                logger.info("Starting long break session")
                self.pomodoro_timer.start(1000)

            elif self.getTimerState() == TimerState.BREAK:
                self.updateSessionProgress()
                self.setTimerDuration(WORK_DURATION * 60 * 1000)
                self.timer_state = TimerState.WORK
                logger.info("Starting work session after break")
                self.pomodoro_timer.start(1000)

            self.timerStateChangedSignal.emit(self.timer_state)

            logger.debug(f"Session Progress (after): {self.session_progress}")
            logger.debug(f"Timer State (after): {self.timer_state}")

    def pauseDuration(self):
        logger.info("Timer is paused now")
        self.pomodoro_timer.stop()

    # handles the end of the work session, break session or long break session
    def durationEnded(self):
        if self.timer_state == TimerState.WORK and self.session_progress < WORK_INTERVALS - 0.5:
            self.startDuration()  # Start the break
        elif self.timer_state == TimerState.WORK and self.session_progress == WORK_INTERVALS - 0.5:
            self.startDuration()  # Start the long break
        elif self.timer_state == TimerState.BREAK:
            self.startDuration()  # Start the work session
        elif self.timer_state == TimerState.LONG_BREAK:
            self.pomodoroSessionEnded()

    # for setting the duration of the timer
    def setTimerDuration(self, duration):
        self.timer_duration = duration

    # for decreasing the remaining time by 1 second since timer timeout is always 1000 milliseconds that is 1 second
    def decreaseRemainingTime(self):
        self.timer_duration -= 1000

        if self.timer_duration < 0:
            self.durationEnded()
            return

        self.getRemainingTime()
        self.pomodoro_timer.start(1000)

    # returns remaining time in seconds for the duration
    def getRemainingTime(self):
        logger.debug(f"Remaining time: {self.timer_duration/1000}")
        return self.timer_duration

    def pomodoroSessionEnded(self):
        logger.info("Pomodoro Session Ended")
        self.stopSession()
        # self.pomodoro_timer.stop()
        # self.session_progress = 0
        # self.timer_state = TimerState.NOTHING
        # logger.debug(f"Session Progress: {self.session_progress}")

    def stopSession(self):
        logger.info("Stopping Pomodoro Session")
        self.pomodoro_timer.stop()
        self.timer_duration = 0
        self.session_progress = 0
        self.timer_state = TimerState.NOTHING
        self.timerStateChangedSignal.emit(self.timer_state)
        logger.debug(f"Session Progress: {self.session_progress}")

    # def skipDuration(self):
    #     logger.info("Skipping duration")
    #     self.timer_duration = 0
    #     self.session_progress += 0.5
    #     self.durationEnded()

if __name__ == '__main__':
    class TestPomodoro:
        def __init__(self):
            self.pomodoro_timer = PomodoroTimer()
            self.pomodoro_timer.startDuration()


    app = QApplication(sys.argv)
    pomodoro_test = TestPomodoro()
    app.exec()
