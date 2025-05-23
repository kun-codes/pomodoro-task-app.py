from PySide6.QtCore import Qt
from qfluentwidgets import BodyLabel, MessageBoxBase, SubtitleLabel

from constants import APPLICATION_NAME
from views.dialogs.setupAppDialog import SetupAppDialog


class PreSetupConfirmationDialog(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = SubtitleLabel(f"Do you want to setup {APPLICATION_NAME} now?", parent=self)
        self.bodyLabel = BodyLabel("During setup you would be temporarily disconnected from the internet.",
                                   parent=self)
        self.bodyLabel2 = BodyLabel("If you are ready, click 'Yes' to start the setup.", parent=self)
        self.bodyLabel3 = BodyLabel(f"If you are not ready, click 'No' to setup later."
                                    f" {APPLICATION_NAME} will close immediately", parent=self)

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.bodyLabel)
        self.viewLayout.addWidget(self.bodyLabel2)
        self.viewLayout.addWidget(self.bodyLabel3)

        self.yesButton.setText("Yes, Setup Now")
        self.cancelButton.setText("No, Setup Later")

        self.initWidget()

    def initWidget(self):
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.bodyLabel.setWordWrap(True)
        self.bodyLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.bodyLabel2.setWordWrap(True)
        self.bodyLabel2.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.bodyLabel3.setWordWrap(True)
        self.bodyLabel3.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.__connectSignalsToSlots()

    def __connectSignalsToSlots(self):
        # disconnecting from the default slots as done in the parent class, so that self.accept() and self.reject()
        # are not called
        self.yesButton.clicked.disconnect()
        self.cancelButton.clicked.disconnect()
        self.yesButton.clicked.connect(self.onYesButtonClicked)
        self.cancelButton.clicked.connect(self.onCancelButtonClicked)

    def onYesButtonClicked(self):
        setup_app_dialog = SetupAppDialog(self)
        if setup_app_dialog.exec():
            self.accept()

    def onCancelButtonClicked(self):
        self.reject()
