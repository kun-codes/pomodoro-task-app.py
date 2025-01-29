from loguru import logger
from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtWidgets import QStackedWidget, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy
from qfluentwidgets import (
    MessageBoxBase,
    SegmentedWidget,
    SubtitleLabel,
    ImageLabel,
    CaptionLabel,
    FlipView,
    PillToolButton,
    FluentIcon,
    TeachingTip,
    InfoBarIcon,
    TeachingTipTailPosition,
    BodyLabel,
)


class TutorialDialog(MessageBoxBase):
    def __init__(self, parent, title: str):
        super().__init__(parent=parent)

        self.title = SubtitleLabel(title, parent=self)
        self.segmentedWidget = SegmentedWidget(parent=self)
        self.stackedWidget = QStackedWidget(parent=self)

        navigationButtonSizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        navigationButtonSizePolicy.setHorizontalStretch(0)
        navigationButtonSizePolicy.setVerticalStretch(0)

        self.imageLayout = QHBoxLayout()
        self.imageLayout.setContentsMargins(0, 0, 0, 0)
        self.imageLayout.setSpacing(0)

        self.leftButton = PillToolButton(parent=self)
        self.leftButton.setSizePolicy(navigationButtonSizePolicy)
        self.leftButton.setMinimumSize(QSize(40, 40))
        self.leftButton.setMaximumSize(QSize(40, 40))
        self.leftButton.setIconSize(QSize(16, 16))
        self.leftButton.setCheckable(False)
        self.leftButton.setIcon(FluentIcon.LEFT_ARROW)
        self.leftButton.clicked.connect(self.showPreviousImage)

        self.rightButton = PillToolButton(parent=self)
        self.rightButton.setSizePolicy(navigationButtonSizePolicy)
        self.rightButton.setMinimumSize(QSize(40, 40))
        self.rightButton.setMaximumSize(QSize(40, 40))
        self.rightButton.setIconSize(QSize(16, 16))
        self.rightButton.setCheckable(False)
        self.rightButton.setIcon(FluentIcon.RIGHT_ARROW)
        self.rightButton.clicked.connect(self.showNextImage)

        self.imageLayout.addWidget(self.leftButton)
        self.imageLayout.addWidget(self.stackedWidget)
        self.imageLayout.addWidget(self.rightButton)

        self.imageLayout.setAlignment(self.stackedWidget, Qt.AlignmentFlag.AlignCenter)

        self.viewLayout.addWidget(self.title)
        self.viewLayout.addLayout(self.imageLayout)

        self.yesButton.hide()

        self.cancelButton.setText("Close")

        # self.widget.resize(int(2 * self.parent().width() / 3), int(2 * self.parent().height() / 3))

        self.__connectSignalsToSlots()

    def __connectSignalsToSlots(self):
        # disconnecting yesButton and cancelButton from the default slots, as they were connected in the parent class
        self.yesButton.clicked.disconnect()
        self.cancelButton.clicked.disconnect()

        self.cancelButton.clicked.connect(self.oncancelButtonClicked)

    def oncancelButtonClicked(self):
        if self.stackedWidget.currentIndex() == self.stackedWidget.count() - 1:
            self.accept()
        else:
            TeachingTip.create(
                self.cancelButton,
                title = "Complete the tutorial first",
                content = "Please complete the tutorial before closing the dialog.",
                icon = InfoBarIcon.INFORMATION,
                isClosable= True,
                tailPosition = TeachingTipTailPosition.TOP,
                parent=self,
                isDeleteOnClose = True
            )

    def addImage(self, imgPath: str, captionText: str, objectName: str, tabText: str):
        containerWidget = QWidget(parent=self)
        containerWidgetLayout = QVBoxLayout(containerWidget)
        containerWidget.setObjectName(objectName)

        imageLabel = ImageLabel(imgPath, parent=self)
        imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        captionLabel = BodyLabel(captionText, self)

        containerWidgetLayout.addWidget(imageLabel)
        containerWidgetLayout.addWidget(captionLabel)

        self.stackedWidget.addWidget(containerWidget)

    def showPreviousImage(self):
        currentIndex = self.stackedWidget.currentIndex()
        if currentIndex > 0:
            self.stackedWidget.setCurrentIndex(currentIndex - 1)

    def showNextImage(self):
        currentIndex = self.stackedWidget.currentIndex()
        if currentIndex < self.stackedWidget.count() - 1:
            self.stackedWidget.setCurrentIndex(currentIndex + 1)

    def show(self):
        super().show()
        self.stackedWidget.setCurrentIndex(0)

