from constants import APPLICATION_NAME
from PySide6.QtCore import Qt
from qfluentwidgets import (
    BodyLabel,
    SubtitleLabel,
    MessageBoxBase,
)


class SetupAppDialogConfirmationDialog(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = SubtitleLabel("Are you sure you have set up website filtering correctly?", parent=self)
        self.bodyLabel = BodyLabel(
            'You can check if the website filter is working correctly by visiting <a href="https://example.com/">https://example.com/</a>',
            parent=self,
        )
        self.bodyLabel2 = BodyLabel(
            f"It should be blocked by {APPLICATION_NAME} if the website filter is working correctly", parent=self
        )

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.bodyLabel)
        self.viewLayout.addWidget(self.bodyLabel2)

        self.yesButton.setText("Yes")
        self.cancelButton.setText("No, Take me back")

        self.initWidget()

    def initWidget(self):

        self.bodyLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.bodyLabel.setOpenExternalLinks(True)
