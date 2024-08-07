from PySide6.QtWidgets import QWidget
from loguru import logger
from qfluentwidgets import FluentIcon, Flyout, InfoBarIcon, FlyoutAnimationType
from sqlalchemy.orm import sessionmaker

from constants import WebsiteFilterType
from models.db_tables import engine, Workspace
from models.website_blocker_model import WebsiteBlockerModel
from models.workspace_list_model import workplace_model
from ui_py.ui_website_blocker_view import Ui_WebsiteBlockView


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

        self.initWidget()
        self.initWebsiteFilterComboBox()
        self.connectSignalsToSlots()

    def initWidget(self):
        self.websiteExceptionHintButton.setIcon(FluentIcon.QUESTION)

    def connectSignalsToSlots(self):
        self.blockTypeComboBox.currentIndexChanged.connect(self.onFilterTypeChanged)
        self.saveButton.clicked.connect(lambda: logger.debug("Save button clicked"))
        self.cancelButton.clicked.connect(lambda: logger.debug("Cancel button clicked"))
        # workplace_model.current_workspace_changed.connect(self.onCurrentWorkplaceChanged)
        workplace_model.current_workspace_deleted.connect(self.onCurrentWorkplaceDeleted)
        self.websiteExceptionHintButton.clicked.connect(self.onExceptionHelpButtonClicked)

    def onExceptionHelpButtonClicked(self):
        Flyout.create(
            icon=InfoBarIcon.INFORMATION,
            title="Exceptions for website filtering",
            content="Add '+' in front of URLs which you want to allow in blocklist and vice versa.",
            target=self.websiteExceptionHintButton,
            parent=self,
            isClosable=False,
            aniType=FlyoutAnimationType.SLIDE_RIGHT
        )

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
        # todo: set blockTypeComboBox index to new current workplace's website_filter_type
        self.blockTypeComboBox.currentIndexChanged.emit(0)
        self.blockListTextEdit.clear()
        # todo: set blockListTextEdit to new current workplace's blocklist
        self.allowListTextEdit.clear()
        # todo: set allowListTextEdit to new current workplace's allowlist
