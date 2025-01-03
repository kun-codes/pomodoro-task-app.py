from constants import APPLICATION_NAME
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QColor, QDesktopServices
from PySide6.QtWidgets import QFrame, QVBoxLayout
from qfluentwidgets import (
    BodyLabel,
    FluentIcon,
    FluentStyleSheet,
    MaskDialogBase,
    PrimaryPushButton,
    PushButton,
    SubtitleLabel,
    setCustomStyleSheet,
)
from views.dialogs.setupAppDialogConfirmationDialog import SetupAppDialogConfirmationDialog


class SetupAppDialog(MaskDialogBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.buttonGroup = QFrame(self.widget)

        # contains both self.viewLayout and self.buttonLayout
        self.vBoxLayout = QVBoxLayout(self.widget)

        self.viewLayout = QVBoxLayout()
        self.buttonLayout = QVBoxLayout(self.buttonGroup)

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
        self.openWebsiteFilterSetupButton = PrimaryPushButton(FluentIcon.LINK, "Open Website Filter Setup", parent=self)
        self.closeDialogButton = PushButton(text="Close", parent=self)

        self.__initWidget()

    def __initWidget(self):
        self.__setQss()
        self.__initLayout()

        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.bodyLabel.setWordWrap(True)
        self.bodyLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.bodyLabel2.setWordWrap(True)
        self.bodyLabel2.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # self.widget.setFixedSize(300, 500)

        self.setShadowEffect(60, (0, 10), QColor(0, 0, 0, 50))
        self.setMaskColor(QColor(0, 0, 0, 76))

        self.__connectSignalsToSlots()

    def __initLayout(self):
        self._hBoxLayout.removeWidget(self.widget)
        self._hBoxLayout.addWidget(self.widget, 1, Qt.AlignCenter)

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addLayout(self.viewLayout, 1)
        self.vBoxLayout.addWidget(self.buttonGroup, 0, Qt.AlignBottom)

        self.viewLayout.setSpacing(12)
        self.viewLayout.setContentsMargins(24, 24, 24, 24)

        self.buttonLayout.setSpacing(12)
        self.buttonLayout.setContentsMargins(24, 24, 24, 24)

        self.viewLayout.addWidget(self.titleLabel, 0, Qt.AlignLeft)
        self.viewLayout.addWidget(self.bodyLabel, 0)
        self.viewLayout.addWidget(self.bodyLabel2, 0)

        self.buttonLayout.addWidget(self.openWebsiteFilterSetupButton)
        self.buttonLayout.addWidget(self.closeDialogButton)

    def __setQss(self):
        self.buttonGroup.setObjectName("buttonGroup")
        dialog_qss = f"""
            {__class__.__name__} #buttonGroup,
            {__class__.__name__} #buttonGroup {{
            border-bottom-left-radius: 8px;
            border-bottom-right-radius: 8px;
        }}
        """
        FluentStyleSheet.DIALOG.apply(self)

        # from: https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/707
        self.style().unpolish(self)
        self.style().polish(self)

        # setStyleSheet()
        setCustomStyleSheet(self, dialog_qss, dialog_qss)

    def __connectSignalsToSlots(self):
        self.openWebsiteFilterSetupButton.clicked.connect(self.onWebsiteFilterSetupButtonClicked)
        self.closeDialogButton.clicked.connect(self.onCloseButtonClicked)

    def onWebsiteFilterSetupButtonClicked(self):
        url = QUrl("https://mitm.it/")
        QDesktopServices.openUrl(url)

    def onCloseButtonClicked(self):
        confirmation_dialog = SetupAppDialogConfirmationDialog(self)

        if confirmation_dialog.exec():
            self.accept()
            # self.close()
