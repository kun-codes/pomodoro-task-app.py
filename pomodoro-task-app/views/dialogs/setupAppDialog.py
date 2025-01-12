from constants import APPLICATION_NAME
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from qfluentwidgets import (
    BodyLabel,
    FluentIcon,
    MessageBoxBase,
    SubtitleLabel,
)
from views.dialogs.setupAppDialogConfirmationDialog import SetupAppDialogConfirmationDialog


class SetupAppDialog(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = SubtitleLabel(f"Setup {APPLICATION_NAME} for the first time", parent=self)
        self.bodyLabel = BodyLabel(
            "Before you start using the app, you need to set up system-wide "
            "website filtering. Click the below button to visit the webpage to set it up",
            parent=self,
        )

        self.bodyLabel2 = BodyLabel(
            "You would need to install mitmproxy's certificate to your system to enable " "website filtering",
            parent=self,
        )
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.bodyLabel)
        self.viewLayout.addWidget(self.bodyLabel2)

        self.yesButton.setText("Open Website Filter Setup")
        self.yesButton.setIcon(FluentIcon.LINK)
        self.cancelButton.setText("Close")

        self.initWidget()

    def initWidget(self):
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.bodyLabel.setWordWrap(True)
        self.bodyLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.bodyLabel2.setWordWrap(True)
        self.bodyLabel2.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # self.widget.setFixedSize(300, 500)

        self.__connectSignalsToSlots()

    def __connectSignalsToSlots(self):
        # disconnecting from the default slots as done in the parent class, so that self.accept() and self.reject()
        # are not called
        self.yesButton.clicked.disconnect()
        self.cancelButton.clicked.disconnect()
        self.yesButton.clicked.connect(self.onWebsiteFilterSetupButtonClicked)
        self.cancelButton.clicked.connect(self.onCloseButtonClicked)

    def onWebsiteFilterSetupButtonClicked(self):
        url = QUrl("https://mitm.it/")
        QDesktopServices.openUrl(url)

    def onCloseButtonClicked(self):
        confirmation_dialog = SetupAppDialogConfirmationDialog(self)

        if confirmation_dialog.exec():
            self.accept()
            # self.close()
