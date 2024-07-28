from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit


class AddTaskDialog(MessageBoxBase):
    """
    For the add task dialog in tasks view
    """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = SubtitleLabel("Add Task", self)
        self.taskEdit = LineEdit(self)

        self.taskEdit.setPlaceholderText("Enter task name")

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.taskEdit)

        self.yesButton.setText("Add Task")
        self.cancelButton.setText("Cancel")

        self.widget.setMinimumWidth(max(350, int(parent.width() * 0.3)))
        self.yesButton.setDisabled(True)
        self.taskEdit.textChanged.connect(self.onTaskTextChanged)

    def onTaskTextChanged(self):
        self.yesButton.setDisabled(self.taskEdit.text().strip() == "")
