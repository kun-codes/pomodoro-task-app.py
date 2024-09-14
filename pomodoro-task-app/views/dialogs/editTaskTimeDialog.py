from PySide6.QtCore import Qt, QTime
from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, TimePicker
from models.task_lookup import TaskLookup


class EditTaskTimeDialog(MessageBoxBase):
    def __init__(self, parent=None, task_id=None):
        super().__init__(parent=parent)

        self.elapsedTimeLabel = SubtitleLabel("Elapsed Time", self)
        self.estimateTimeLabel = SubtitleLabel("Estimated Time", self)

        self.elapsedTimePicker = TimePicker(self)
        self.estimateTimePicker = TimePicker(self)

        elapsed_time = TaskLookup.get_elapsed_time(task_id)
        target_time = TaskLookup.get_target_time(task_id)

        # convert ms to QTime
        elapsed_time_qtime = self.convertMsToQTime(elapsed_time)
        target_time_qtime = self.convertMsToQTime(target_time)

        self.elapsedTimePicker.setTime(elapsed_time_qtime)
        self.estimateTimePicker.setTime(target_time_qtime)

        self.viewLayout.addWidget(self.elapsedTimeLabel)
        self.viewLayout.addWidget(self.elapsedTimePicker)
        self.viewLayout.addWidget(self.estimateTimeLabel)
        self.viewLayout.addWidget(self.estimateTimePicker)

    def convertMsToQTime(self, ms):
        seconds = ms // 1000
        minute, second = divmod(seconds, 60)
        hour, minute = divmod(minute, 60)
        return QTime(hour, minute, second)

    def getElapsedTime(self):
        time =  self.elapsedTimePicker.getTime()
        return (time.hour() * 60 * 60 + time.minute() * 60 + time.second()) * 1000

    def getTargetTime(self):
        time =  self.estimateTimePicker.getTime()
        return (time.hour() * 60 * 60 + time.minute() * 60 + time.second()) * 1000



if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dialog = AddTaskDialog()
    dialog.exec()
    sys.exit(app.exec())

