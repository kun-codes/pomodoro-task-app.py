from PySide6.QtWidgets import QWidget, QStackedWidget
from PySide6.QtCore import Qt
from enum import Enum
from sqlalchemy.orm import sessionmaker
from models.db_tables import engine, Workspace

from ui_py.ui_website_blocker_view import Ui_WebsiteBlockView
from qfluentwidgets import PlainTextEdit, Pivot
from loguru import logger
from constants import WebsiteFilterType
from models.workspace_list_model import workplace_model
from models.website_blocker_model import WebsiteBlockerModel

class WebsiteBlockerView(Ui_WebsiteBlockView, QWidget):
    """
    For website blocker view of the app
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # for testing
        self.blockListTextEdit.setPlainText("Blocklist")
        self.allowListTextEdit.setPlainText("Allowlist")

        self.blockListTextEdit.setHidden(True)
        self.allowListTextEdit.setHidden(True)

        current_workspace_id = workplace_model.get_current_workspace_id()
        session = sessionmaker(bind=engine)()
        self.workplaceBlockTypePreference = session.query(Workspace).get(current_workspace_id).website_filter_type
        logger.debug(f"Workplace block type preference in __init__: {self.workplaceBlockTypePreference}")
        session.close()

        self.model = WebsiteBlockerModel()

        self.initWebsiteFilterComboBox()
        self.connectSignalsToSlots()
                                                            # still emit the signal to show/hide appropriate widgets

    def connectSignalsToSlots(self):
        self.blockTypeComboBox.currentIndexChanged.connect(self.onFilterTypeChanged)
        self.saveButton.clicked.connect(lambda: logger.debug("Save button clicked"))
        self.cancelButton.clicked.connect(lambda: logger.debug("Cancel button clicked"))
        # workplace_model.current_workspace_changed.connect(self.onCurrentWorkplaceChanged)
        workplace_model.current_workspace_deleted.connect(self.onCurrentWorkplaceDeleted)

    def load_data(self):
        # todo: don't let user change filter type till they click on save button
        # todo: don't let user click on save button till they make some changes
        # todo: check for invalid urls
        # todo: check for duplicate urls
        pass

    def onFilterTypeChanged(self):
        if self.blockTypeComboBox.currentIndex() == WebsiteFilterType.BLOCKLIST.value:
            self.allowListTextEdit.setHidden(True)
            self.blockListTextEdit.setHidden(False)

            self.model.set_website_filter_type(WebsiteFilterType.BLOCKLIST)
            self.workplaceBlockTypePreference = WebsiteFilterType.BLOCKLIST

        elif self.blockTypeComboBox.currentIndex() == WebsiteFilterType.ALLOWLIST.value:
            self.allowListTextEdit.setHidden(False)
            self.blockListTextEdit.setHidden(True)

            self.model.set_website_filter_type(WebsiteFilterType.ALLOWLIST)
            self.workplaceBlockTypePreference = WebsiteFilterType.ALLOWLIST


    def initWebsiteFilterComboBox(self):
        self.blockTypeComboBox.addItem("Blocklist")
        self.blockTypeComboBox.addItem("Allowlist")

        self.blockTypeComboBox.setCurrentIndex(self.workplaceBlockTypePreference.value)
        self.onFilterTypeChanged()  # calling manually since signals aren't connected to slots yet

    def onCurrentWorkplaceDeleted(self):
        # set every ui component to its default
        self.blockTypeComboBox.setCurrentIndex(0)
        self.blockTypeComboBox.currentIndexChanged.emit(0)
        self.blockListTextEdit.clear()
        self.allowListTextEdit.clear()
