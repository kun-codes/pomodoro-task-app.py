from qfluentwidgets import HorizontalFlipView, MessageBoxBase, SubtitleLabel


class TutorialDialog(MessageBoxBase):
    def __init__(self, parent, title: str):
        super().__init__(parent=parent)

        self.title = SubtitleLabel(title, parent=self)
        self.flipView = HorizontalFlipView(parent=self)

        self.viewLayout.addWidget(self.title)
        self.viewLayout.addWidget(self.flipView)

        self.yesButton.hide()

        self.cancelButton.setText("Close")

        self.__connectSignalsToSlots()

    def __connectSignalsToSlots(self):
        # disconnecting yesButton and cancelButton from the default slots, as they were connected in the parent class
        self.yesButton.clicked.disconnect()
        self.cancelButton.clicked.disconnect()

        self.cancelButton.clicked.connect(self.oncancelButtonClicked)

    def oncancelButtonClicked(self):
        self.accept()
