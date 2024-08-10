from PySide6.QtWidgets import QWidget
from qfluentwidgets import FluentIcon, Flyout, InfoBarIcon, FlyoutAnimationType

from constants import WebsiteFilterType, URLListType
from models.db_tables import engine, Workspace
from models.website_blocker_model import WebsiteBlockerModel
from models.workspace_list_model import workspace_list_model
from ui_py.ui_website_blocker_view import Ui_WebsiteBlockView
from utils.db_utils import get_session


class WebsiteBlockerView(Ui_WebsiteBlockView, QWidget):
    """
    For website blocker view of the app
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.blockListText = ""
        self.allowListText = ""

        current_workspace_id = workspace_list_model.get_current_workspace_id()
        with get_session(is_read_only=True) as session:
            self.workspaceBlockTypePreference = session.query(Workspace).get(current_workspace_id).website_filter_type

        self.model = WebsiteBlockerModel()

        self.initWidget()
        self.connectSignalsToSlots()

        self.saveButton.setDisabled(True)

    def initWidget(self):
        self.websiteExceptionHintButton.setIcon(FluentIcon.QUESTION)

        self.blockListTextEdit.setHidden(True)
        self.allowListTextEdit.setHidden(True)

        self.initTextEdits()
        self.initWebsiteFilterComboBox()

    def connectSignalsToSlots(self):
        self.blockTypeComboBox.currentIndexChanged.connect(self.onFilterTypeChanged)
        self.saveButton.clicked.connect(self.onSaveButtonClicked)
        self.cancelButton.clicked.connect(self.onCancelButtonClicked)
        # workspace_model.current_workspace_changed.connect(self.onCurrentWorkspaceChanged)
        workspace_list_model.current_workspace_deleted.connect(self.onCurrentWorkspaceDeleted)
        self.websiteExceptionHintButton.clicked.connect(self.onExceptionHelpButtonClicked)

        self.blockListTextEdit.textChanged.connect(self.onTextChanged)
        self.allowListTextEdit.textChanged.connect(self.onTextChanged)

    def onTextChanged(self):
        self.saveButton.setDisabled(False)
        self.blockTypeComboBox.setDisabled(True)
        # todo: show the user a tip that they can enable the combo box again by clicking on save or cancel buttons

    def onSaveButtonClicked(self):
        self.blockListText = self.blockListTextEdit.toPlainText().strip()
        self.allowListText = self.allowListTextEdit.toPlainText().strip()

        self.blockListText = '\n'.join(sorted(self.blockListText.split('\n')))
        self.allowListText = '\n'.join(sorted(self.allowListText.split('\n')))

        self.blockListTextEdit.setPlainText(self.blockListText)
        self.allowListTextEdit.setPlainText(self.allowListText)

        current_website_filter_type = self.model.get_website_filter_type()
        if current_website_filter_type == WebsiteFilterType.BLOCKLIST:
            # assuming all urls are separated by new line and are valid
            list_of_urls = [url.strip() for url in self.blockListText.split('\n') if url.strip()]
            self.model.update_target_list_urls(URLListType.BLOCKLIST, list_of_urls)
        elif current_website_filter_type == WebsiteFilterType.ALLOWLIST:
            list_of_urls = [url.strip() for url in self.allowListText.split('\n') if url.strip()]
            self.model.update_target_list_urls(URLListType.ALLOWLIST, list_of_urls)

        self.saveButton.setDisabled(True)
        self.blockTypeComboBox.setDisabled(False)

    def onCancelButtonClicked(self):
        self.blockListTextEdit.setPlainText(self.blockListText)
        self.allowListTextEdit.setPlainText(self.allowListText)

        self.saveButton.setDisabled(True)
        self.blockTypeComboBox.setDisabled(False)

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
            self.workspaceBlockTypePreference = WebsiteFilterType.BLOCKLIST

        elif self.blockTypeComboBox.currentIndex() == WebsiteFilterType.ALLOWLIST.value:
            self.allowListTextEdit.setHidden(False)
            self.blockListTextEdit.setHidden(True)

            self.model.set_website_filter_type(WebsiteFilterType.ALLOWLIST)
            self.workspaceBlockTypePreference = WebsiteFilterType.ALLOWLIST

    def initWebsiteFilterComboBox(self):
        self.blockTypeComboBox.addItem("Blocklist")
        self.blockTypeComboBox.addItem("Allowlist")

        self.blockTypeComboBox.setCurrentIndex(self.workspaceBlockTypePreference.value)
        self.onFilterTypeChanged()  # calling manually since signals aren't connected to slots yet

    def initTextEdits(self):
        self.blockListTextEdit.setPlainText("\n".join(sorted(self.model.blocklist_urls)))
        self.allowListTextEdit.setPlainText("\n".join(sorted(self.model.allowlist_urls)))

        self.blockListText = self.blockListTextEdit.toPlainText()
        self.allowListText = self.allowListTextEdit.toPlainText()

    def onCurrentWorkspaceDeleted(self):
        # set every ui component to its default
        self.blockTypeComboBox.setCurrentIndex(0)
        # todo: set blockTypeComboBox index to new current workspace's website_filter_type
        self.blockTypeComboBox.currentIndexChanged.emit(0)
        self.blockListTextEdit.clear()
        # todo: set blockListTextEdit to new current workspace's blocklist
        self.allowListTextEdit.clear()
        # todo: set allowListTextEdit to new current workspace's allowlist
