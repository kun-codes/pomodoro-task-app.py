from constants import APPLICATION_NAME
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QFrame, QVBoxLayout
from qfluentwidgets import (
    BodyLabel,
    FluentStyleSheet,
    MaskDialogBase,
    PrimaryPushButton,
    PushButton,
    SubtitleLabel,
    setCustomStyleSheet,
)


class SetupAppDialogConfirmationDialog(MaskDialogBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.buttonGroup = QFrame(self.widget)

        # contains both self.viewLayout and self.buttonLayout
        self.vBoxLayout = QVBoxLayout(self.widget)

        self.viewLayout = QVBoxLayout()
        self.buttonLayout = QVBoxLayout(self.buttonGroup)

        self.titleLabel = SubtitleLabel("Are you sure you have set up website filtering correctly?", parent=self)
        self.bodyLabel = BodyLabel(
            'You can check if the website filter is working correctly by visiting <a href="https://example.com/">https://example.com/</a>',
            parent=self,
        )
        self.bodyLabel2 = BodyLabel(
            f"It should be blocked by {APPLICATION_NAME} if the website filter is working correctly", parent=self
        )

        self.okayButton = PrimaryPushButton(text="Yes", parent=self)
        self.cancelButton = PushButton("No, Take me back", parent=self)

        self.__initWidget()

    def __initWidget(self):
        self.__setQss()
        self.__initLayout()

        self.bodyLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.bodyLabel.setOpenExternalLinks(True)

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
        self.viewLayout.addWidget(self.bodyLabel, 0, Qt.AlignLeft)
        self.viewLayout.addWidget(self.bodyLabel2, 0, Qt.AlignLeft)

        self.buttonLayout.addWidget(self.okayButton)
        self.buttonLayout.addWidget(self.cancelButton)

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
        self.okayButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
