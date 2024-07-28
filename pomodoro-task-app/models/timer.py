import sys
from enum import Enum

from PySide6.QtCore import QTimer, Signal, QObject
from PySide6.QtWidgets import QApplication
from loguru import logger

from config_values import ConfigValues


# Enum which tells what state the timer is in
class TimerState(Enum):
    NOTHING = "Begin Timer"
    WORK = "Focus"
    BREAK = "Break"
    LONG_BREAK = "Long Break"


class PomodoroTimer(QObject):  # Inherit from QObject to support signals
    # first argument for current timer state
    timerStateChangedSignal = Signal(TimerState)
    sessionEndedSignal = Signal()
    waitForUserInputSignal = Signal()

    def __init__(self):
        super().__init__()
        self.timer_state = TimerState.NOTHING
        self.pomodoro_timer = QTimer()
        self.session_progress = 0  # would be incremented by 0.5 after every work ended signal is emitted
        # would also be incremented by 0.5 after every break ended signal is emitted
        # starts out at 0 which means that the timer state is NOTHING
        # whole number means that break is going on
        # would be reset to zero after every long break

        self.remaining_time = 0  # will change according to BREAK_DURATION, WORK_DURATION, LONG_BREAK_DURATION
        self.timer_resolution = 100  # in milliseconds

        # self.pomodoro_timer.timeout.connect(self.sessionEnded)
        self.pomodoro_timer.timeout.connect(self.decreaseRemainingTime)

    def getTimerState(self):
        return self.timer_state

    # increments the session tracking variable session_progress by 0.5 or resets to 0 depending on the timer state
    def updateSessionProgress(self):
        logger.debug(f"Session Progress (before): {self.session_progress}")
        logger.debug(f"Timer State (before): {self.timer_state}")

        if self.timer_state == TimerState.WORK:
            if self.session_progress < ConfigValues.WORK_INTERVALS - 0.5:
                self.session_progress += 0.5
                self.timer_state = TimerState.BREAK
            elif self.session_progress == ConfigValues.WORK_INTERVALS - 0.5:
                self.session_progress += 0.5
                self.timer_state = TimerState.LONG_BREAK
        elif self.timer_state == TimerState.BREAK:
            self.session_progress += 0.5
            self.timer_state = TimerState.WORK
        elif self.timer_state == TimerState.NOTHING:
            self.session_progress += 0.5
            self.timer_state = TimerState.WORK
        elif self.timer_state == TimerState.LONG_BREAK:
            self.session_progress += 0.5  # Back to work after long_break
            self.timer_state = TimerState.WORK

        self.session_progress = self.session_progress % ConfigValues.WORK_INTERVALS  # for example in case work intervals is
        # 2 and during long break it was 2 and then after it, it becomes 2.5 which is not a valid state, so we get the
        # remainder which is 0.5

        self.timerStateChangedSignal.emit(self.timer_state)

    # starts the timer for the work session, break session or long break session
    def setDuration(self):
        if self.remaining_time > 0 and not self.pomodoro_timer.isActive():  # if timer is paused
            logger.info("Resuming timer")
            self.pomodoro_timer.start(self.timer_resolution)
        else:  # if timer is not paused then set timer duration and start timer
            if self.getTimerState() == TimerState.NOTHING:
                logger.info("In Nothing State")
            elif self.getTimerState() == TimerState.WORK:
                logger.debug(f"Work duration: {ConfigValues.WORK_DURATION}")
                self.setTimerDuration(ConfigValues.WORK_DURATION * 60 * 1000)
                logger.info("Starting work session")
            elif self.getTimerState() == TimerState.BREAK:
                logger.debug(f"Break duration: {ConfigValues.BREAK_DURATION}")
                self.setTimerDuration(ConfigValues.BREAK_DURATION * 60 * 1000)
                logger.info("Starting break session")
            elif self.getTimerState() == TimerState.LONG_BREAK:
                logger.debug(f"Long break duration: {ConfigValues.LONG_BREAK_DURATION}")
                self.setTimerDuration(ConfigValues.LONG_BREAK_DURATION * 60 * 1000)
                logger.info("Starting long break session")

            logger.debug(f"Session Progress (after): {self.session_progress}")
            logger.debug(f"Timer State (after): {self.timer_state}")

    def startDuration(self):
        self.pomodoro_timer.start(self.timer_resolution)

    def pauseDuration(self):
        logger.info("Timer is paused now")
        self.pomodoro_timer.stop()

    # handles the end of the work session, break session or long break session
    def durationEnded(self, isSkipped=False):
        self.pomodoro_timer.stop()
        if self.timer_state == TimerState.WORK:
            self.updateSessionProgress()
            self.setDuration()
            if isSkipped:  # if session is skipped then value of autostart_break is not checked as it doesn't matter
                # and start the next duration automatically
                self.startDuration()
                return
            elif ConfigValues.AUTOSTART_BREAK:
                logger.info("Auto-starting break session")
                self.startDuration()
            else:
                logger.info("Waiting for user input after ending work session")
                self.waitForUserInputSignal.emit()  # resets the pause resume button to its checked state
                self.timerStateChangedSignal.emit(self.timer_state)
        elif self.timer_state in [TimerState.BREAK, TimerState.LONG_BREAK]:
            self.updateSessionProgress()
            self.setDuration()
            if isSkipped:
                self.startDuration()
                return
            if ConfigValues.AUTOSTART_WORK:
                logger.info("Auto-starting work session")
                self.startDuration()
            else:
                logger.info("Waiting for user input after ending break session")
                self.waitForUserInputSignal.emit()
                self.timerStateChangedSignal.emit(self.timer_state)

    def skipDuration(self):
        if self.remaining_time == 0 and not self.pomodoro_timer.isActive():
            # TODO: Implement skipping duration when timer is not doing anything
            raise NotImplementedError("Skipping duration when timer is not doing anything isn't implemented currently")
            logger.info("Skipping duration when timer is doing nothing")
        else:
            logger.info("Skipping duration when timer is doing something")
            self.remaining_time = 0
            self.durationEnded(isSkipped=True)

    # for setting the duration of the timer
    def setTimerDuration(self, duration):
        self.remaining_time = duration

    # for decreasing the remaining time by 1 second since timer timeout is always 1000 milliseconds that is 1 second
    def decreaseRemainingTime(self):
        if __name__ == '__main__':
            logger.debug(f"Remaining time (in seconds): {self.getRemainingTime() / 1000}")

        self.remaining_time -= self.timer_resolution

        if self.remaining_time < 0:
            self.durationEnded()
            return

        self.pomodoro_timer.start(self.timer_resolution)

    # returns remaining time in milliseconds for the duration
    def getRemainingTime(self):
        return self.remaining_time

    def pomodoroSessionEnded(self):
        logger.info("Pomodoro Session Ended")
        self.stopSession()

    def stopSession(self):
        logger.info("Stopping Pomodoro Session")
        self.pomodoro_timer.stop()
        self.remaining_time = 0
        self.session_progress = 0
        self.timer_state = TimerState.NOTHING
        self.timerStateChangedSignal.emit(self.timer_state)
        self.sessionEndedSignal.emit()
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
            self.pomodoro_timer.updateSessionProgress()
            self.pomodoro_timer.setDuration()
            self.pomodoro_timer.startDuration()


    app = QApplication(sys.argv)
    pomodoro_test = TestPomodoro()
    app.exec()