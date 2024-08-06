from PySide6.QtWidgets import QWidget, QStackedWidget
from PySide6.QtCore import Qt
from enum import Enum
from ui_py.ui_website_blocker_view import Ui_WebsiteBlockView
from qfluentwidgets import PlainTextEdit, Pivot
from loguru import logger

from constants import WebsiteFilterType
from models.workspace_list_model import workplace_model

class WebsiteBlockerView(Ui_WebsiteBlockView, QWidget):
    """
    For website blocker view of the app
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.blockListTextEdit = PlainTextEdit()
        self.blockListTextEdit.setObjectName("BlocklistTextEdit")
        self.blockListExceptionsTextEdit = PlainTextEdit()
        self.blockListExceptionsTextEdit.setObjectName("BlocklistExceptionsTextEdit")
        self.allowListTextEdit = PlainTextEdit()
        self.allowListTextEdit.setObjectName("AllowlistTextEdit")
        self.allowListExceptionsTextEdit = PlainTextEdit()
        self.allowListExceptionsTextEdit.setObjectName("AllowlistExceptionsTextEdit")

        # for testing
        self.blockListTextEdit.setPlainText("Blocklist")
        self.blockListExceptionsTextEdit.setPlainText("Blocklist Exceptions")
        self.allowListTextEdit.setPlainText("Allowlist")
        self.allowListExceptionsTextEdit.setPlainText("Allowlist Exceptions")

        self.workplaceBlockTypePreference = 0  # TODO: add a block type preference to workplace table

        self.initPivot()
        self.connectSignalsToSlots()
        self.initWebsiteFilterComboBox()
                                                            # still emit the signal to show/hide appropriate widgets

    def connectSignalsToSlots(self):
        self.blockTypeComboBox.currentIndexChanged.connect(self.onBlockTypeChanged)
        self.saveButton.clicked.connect(lambda: logger.debug("Save button clicked"))
        self.cancelButton.clicked.connect(lambda: logger.debug("Cancel button clicked"))

    def onBlockTypeChanged(self):
        if self.blockTypeComboBox.currentText() == WebsiteFilterType.BLOCKLIST.value:
            self.blocklistPivot.show()
            self.blocklistStackedWidget.show()
            self.allowlistPivot.hide()
            self.allowlistStackedWidget.hide()

            self.blocklistPivot.setCurrentItem(self.blockListTextEdit.objectName())
            self.blocklistStackedWidget.setCurrentWidget(self.blockListTextEdit)

            current_workspace_id = workplace_model.get_current_workspace_id()

        elif self.blockTypeComboBox.currentText() == WebsiteFilterType.ALLOWLIST.value:
            self.blocklistPivot.hide()
            self.blocklistStackedWidget.hide()
            self.allowlistPivot.show()
            self.allowlistStackedWidget.show()

            self.allowlistPivot.setCurrentItem(self.allowListTextEdit.objectName())
            self.allowlistStackedWidget.setCurrentWidget(self.allowListTextEdit)

    def initWebsiteFilterComboBox(self):
        self.blockTypeComboBox.addItem(WebsiteFilterType.BLOCKLIST.value)
        self.blockTypeComboBox.addItem(WebsiteFilterType.ALLOWLIST.value)

        self.blockTypeComboBox.setCurrentIndex(self.workplaceBlockTypePreference)
        self.blockTypeComboBox.currentIndexChanged.emit(self.workplaceBlockTypePreference)  # if block list type is
        # already set, then emit the signal explicitly to show/hide the appropriate widgets

    def initPivot(self):
        self.addSubInterface(self.blocklistPivot, self.blocklistStackedWidget, self.blockListTextEdit, 'Blocklist')
        self.addSubInterface(self.blocklistPivot, self.blocklistStackedWidget, self.blockListExceptionsTextEdit, 'Blocklist Exceptions')
        self.addSubInterface(self.allowlistPivot, self.allowlistStackedWidget, self.allowListTextEdit, 'Allowlist')
        self.addSubInterface(self.allowlistPivot, self.allowlistStackedWidget, self.allowListExceptionsTextEdit, 'Allowlist Exceptions')


    def addSubInterface(self, pivot: Pivot, stackedWidget: QStackedWidget, widget: PlainTextEdit, text: str):
        stackedWidget.addWidget(widget)

        # Use the globally unique objectName as the route key
        pivot.addItem(
            routeKey=widget.objectName(),
            text=text,
            onClick=lambda: stackedWidget.setCurrentWidget(widget)
        )

