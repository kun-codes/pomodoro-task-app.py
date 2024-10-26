from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from qfluentwidgets import FluentIcon, Flyout, InfoBarIcon, FlyoutAnimationType, InfoBar, InfoBadgePosition, \
    InfoBarPosition

from constants import WebsiteFilterType, URLListType
from models.website_list_manager_model import WebsiteListManager
from models.workspace_list_model import WorkspaceListModel
from ui_py.ui_website_blocker_view import Ui_WebsiteBlockView
from models.workspace_lookup import WorkspaceLookup
from loguru import logger

class WebsiteBlockerView(Ui_WebsiteBlockView, QWidget):
    """
    For website blocker view of the app
    """

    def __init__(self, workspace_list_model: WorkspaceListModel):
        super().__init__()
        self.setupUi(self)

        self.blockListText = ""
        self.allowListText = ""

        self.model = WebsiteListManager()
        self.workspace_list_model = workspace_list_model

        self.initWidget()
        self.connectSignalsToSlots()

        self.model.invalidURLSignal.connect(self.onInvalidURLSignal)

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
        self.workspace_list_model.current_workspace_deleted.connect(self.onCurrentWorkspaceDeleted)
        self.workspace_list_model.current_workspace_changed.connect(self.onCurrentWorkspaceChanged)
        self.websiteExceptionHintButton.clicked.connect(self.onExceptionHelpButtonClicked)

        self.blockListTextEdit.textChanged.connect(self.onTextChanged)
        self.allowListTextEdit.textChanged.connect(self.onTextChanged)

    def onTextChanged(self):
        self.saveButton.setDisabled(False)
        self.blockTypeComboBox.setDisabled(True)
        # todo: show the user a tip that they can enable the combo box again by clicking on save or cancel buttons

    def onSaveButtonClicked(self):
        blockListTextBeforeSave = self.blockListTextEdit.toPlainText().strip()
        allowListTextBeforeSave = self.allowListTextEdit.toPlainText().strip()

        current_website_filter_type = self.model.get_website_filter_type()

        if current_website_filter_type == WebsiteFilterType.BLOCKLIST:
            urls = []
            block_count = self.blockListTextEdit.blockCount()
            for i in range(block_count):
                block = self.blockListTextEdit.document().findBlockByNumber(i)
                urls.append(block.text())
            # problems in showing the line numbers of invalid urls
            # using list comprehension instead of set comprehension to maintain the order of urls
        elif current_website_filter_type == WebsiteFilterType.ALLOWLIST:
            urls = []
            block_count = self.allowListTextEdit.blockCount()
            for i in range(block_count):
                block = self.allowListTextEdit.document().findBlockByNumber(i)
                urls.append(block.text())

        is_all_urls_valid = self.model.validate_urls(urls)
        if not is_all_urls_valid:
            # InvalidURLSignal will be emitted and trigger onInvalidURLSignal() method
            return  # return and don't save the urls

        # urls are now valid
        urls = set(urls)  # converting to set as self.model.update_target_list_urls() expects a set
        urls = {url.strip() for url in urls if url.strip()}  # removing empty strings and strings with only whitespaces

        if current_website_filter_type == WebsiteFilterType.BLOCKLIST:
            self.model.update_target_list_urls(URLListType.BLOCKLIST, urls)
            self.initTextEdits(WebsiteFilterType.BLOCKLIST)
        elif current_website_filter_type == WebsiteFilterType.ALLOWLIST:
            self.model.update_target_list_urls(URLListType.ALLOWLIST, urls)
            self.initTextEdits(WebsiteFilterType.ALLOWLIST)

        self.saveButton.setDisabled(True)
        self.blockTypeComboBox.setDisabled(False)

        InfoBar.success(
            "URLs saved",
            f"URLs for {"blocklist" if current_website_filter_type == WebsiteFilterType.BLOCKLIST \
                else "allowlist"} has been saved successfully.",
            orient=Qt.Orientation.Vertical,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=4000,
            parent=self
        )

    def onInvalidURLSignal(self, line_numbers: list[int]):
        # show infobar
        InfoBar.error(
            "Invalid URLs",
    f"URLs at line numbers {', '.join(map(str, line_numbers[:10]))}"
            f"{'...' if len(line_numbers) > 10 else ''} are invalid.",  # only show first 10 invalid url,
            # if there are more than 10 that then show ... after the first 10 invalid url line numbers
            orient=Qt.Orientation.Vertical,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=4000,
            parent=self
        )

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
        # todo: check for invalid urls
        pass

    def onFilterTypeChanged(self):
        logger.debug("Inside onFilterTypeChanged")
        if self.blockTypeComboBox.currentIndex() == WebsiteFilterType.BLOCKLIST.value:
            self.allowListTextEdit.setHidden(True)
            self.blockListTextEdit.setHidden(False)

            self.model.set_website_filter_type(WebsiteFilterType.BLOCKLIST)

        elif self.blockTypeComboBox.currentIndex() == WebsiteFilterType.ALLOWLIST.value:
            self.allowListTextEdit.setHidden(False)
            self.blockListTextEdit.setHidden(True)

            self.model.set_website_filter_type(WebsiteFilterType.ALLOWLIST)

    def initWebsiteFilterComboBox(self):
        self.blockTypeComboBox.addItem("Blocklist")
        self.blockTypeComboBox.addItem("Allowlist")

        self.blockTypeComboBox.setCurrentIndex(self.model.get_website_filter_type().value)
        self.onFilterTypeChanged()  # calling manually since signals aren't connected to slots yet

    def initTextEdits(self, filter_type: WebsiteFilterType = None):
        if filter_type == None:
            self.blockListTextEdit.setPlainText("\n".join(sorted(self.model.blocklist_urls)))
            self.allowListTextEdit.setPlainText("\n".join(sorted(self.model.allowlist_urls)))

            self.blockListText = self.blockListTextEdit.toPlainText()
            self.allowListText = self.allowListTextEdit.toPlainText()
        elif filter_type == WebsiteFilterType.BLOCKLIST:
            self.blockListTextEdit.setPlainText("\n".join(sorted(self.model.blocklist_urls)))
            self.blockListText = self.blockListTextEdit.toPlainText()
        elif filter_type == WebsiteFilterType.ALLOWLIST:
            self.allowListTextEdit.setPlainText("\n".join(sorted(self.model.allowlist_urls)))
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

    def onCurrentWorkspaceChanged(self):
        self.model.load_website_filter_type()
        self.model.load_data()

        current_workspace = WorkspaceLookup.get_current_workspace()
        self.blockTypeComboBox.setCurrentIndex(current_workspace.website_filter_type.value)

        self.initTextEdits()

        self.saveButton.setDisabled(True)
        self.blockTypeComboBox.setDisabled(False)
