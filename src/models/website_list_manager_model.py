from urllib.parse import urlparse

import validators
from loguru import logger
from PySide6.QtCore import QObject

from constants import URLListType, WebsiteFilterType
from models.db_tables import AllowlistExceptionURL, AllowlistURL, BlocklistExceptionURL, BlocklistURL, Workspace
from models.workspace_lookup import WorkspaceLookup
from utils.db_utils import get_session


class WebsiteListManager(QObject):
    def __init__(self):
        super().__init__()

        self.blocklist_urls = set()
        self.blocklist_exception_urls = set()
        self.allowlist_urls = set()
        self.allowlist_exception_urls = set()

        self.website_filter_type = None

        self.load_website_filter_type()
        self.load_data()

    def load_data(self, target_list: URLListType = None):
        with get_session(is_read_only=True) as session:
            current_workspace_id = WorkspaceLookup.get_current_workspace_id()

            if target_list is None:
                self.blocklist_urls = {
                    url.url
                    for url in session.query(BlocklistURL)
                    .filter(BlocklistURL.workspace_id == current_workspace_id)
                    .all()
                }
                self.blocklist_exception_urls = {
                    url.url
                    for url in session.query(BlocklistExceptionURL)
                    .filter(BlocklistExceptionURL.workspace_id == current_workspace_id)
                    .all()
                }
                self.allowlist_urls = {
                    url.url
                    for url in session.query(AllowlistURL)
                    .filter(AllowlistURL.workspace_id == current_workspace_id)
                    .all()
                }
                self.allowlist_exception_urls = {
                    url.url
                    for url in session.query(AllowlistExceptionURL)
                    .filter(AllowlistExceptionURL.workspace_id == current_workspace_id)
                    .all()
                }
            elif target_list == URLListType.BLOCKLIST:
                self.blocklist_urls = {
                    url.url
                    for url in session.query(BlocklistURL)
                    .filter(BlocklistURL.workspace_id == current_workspace_id)
                    .all()
                }
                logger.debug("Inside if condition of load_data() for BLOCKLIST")
            elif target_list == URLListType.BLOCKLIST_EXCEPTION:
                self.blocklist_exception_urls = {
                    url.url
                    for url in session.query(BlocklistExceptionURL)
                    .filter(BlocklistExceptionURL.workspace_id == current_workspace_id)
                    .all()
                }
            elif target_list == URLListType.ALLOWLIST:
                self.allowlist_urls = {
                    url.url
                    for url in session.query(AllowlistURL)
                    .filter(AllowlistURL.workspace_id == current_workspace_id)
                    .all()
                }
            elif target_list == URLListType.ALLOWLIST_EXCEPTION:
                self.allowlist_exception_urls = {
                    url.url
                    for url in session.query(AllowlistExceptionURL)
                    .filter(AllowlistExceptionURL.workspace_id == current_workspace_id)
                    .all()
                }

    def load_website_filter_type(self):
        with get_session(is_read_only=True) as session:
            current_workspace_id = WorkspaceLookup.get_current_workspace_id()
            self.website_filter_type = session.query(Workspace).get(current_workspace_id).website_filter_type

    def set_website_filter_type(self, website_filter_type: WebsiteFilterType):
        with get_session() as session:
            current_workspace = WorkspaceLookup.get_current_workspace()
            current_workspace.website_filter_type = website_filter_type
            session.add(current_workspace)
            self.website_filter_type = website_filter_type

    def get_website_filter_type(self):
        return self.website_filter_type

    def update_target_list_urls(self, target_list: URLListType, target_list_urls: set):
        """
        This method updates the target list of urls with the new set of urls. It assumes that all urls are valid.
        Use validate_urls() to check if the urls are valid before calling this method.
        """
        with get_session() as session:
            current_urls = set()
            target_class = None

            if target_list == URLListType.BLOCKLIST:
                current_urls = self.blocklist_urls
                target_class = BlocklistURL
            elif target_list == URLListType.BLOCKLIST_EXCEPTION:
                current_urls = self.blocklist_exception_urls
                target_class = BlocklistExceptionURL
            elif target_list == URLListType.ALLOWLIST:
                current_urls = self.allowlist_urls
                target_class = AllowlistURL
            elif target_list == URLListType.ALLOWLIST_EXCEPTION:
                current_urls = self.allowlist_exception_urls
                target_class = AllowlistExceptionURL

            urls_to_add = target_list_urls - current_urls  # new url = url not in old set but in new set
            urls_to_remove = current_urls - target_list_urls  # removed url = url not in new set but in old set

            if urls_to_remove:
                self.remove_urls(session, urls_to_remove, target_class)

            if urls_to_add:
                self.add_urls(session, urls_to_add, target_class)

        self.load_data(target_list)

    # helper function for validate_url()
    def add_default_scheme(self, url):
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            return f"https://{url}"
        return url

    def validate_urls(self, urls: list):
        invalid_urls_line_numbers = list()
        for n, url in enumerate(urls, start=1):
            # logger.debug(f"{n} {url} empty?={not url}")
            if not url.strip():  # skip empty strings
                continue

            url = self.add_default_scheme(url)  # add default scheme if not present

            if not validators.url(url):
                invalid_urls_line_numbers.append(n)

        logger.debug(f"Invalid urls: {invalid_urls_line_numbers}")

        if invalid_urls_line_numbers:
            return False, invalid_urls_line_numbers
        else:
            return True, None  # returning None as there are no invalid urls

    # helper function for update_target_list_urls()
    def add_urls(self, session, urls: set, target_class):
        for url in urls:
            session.add(target_class(workspace_id=WorkspaceLookup.get_current_workspace_id(), url=url))

    # helper function for update_target_list_urls()
    def remove_urls(self, session, urls: set, target_class):
        session.query(target_class).filter(
            target_class.url.in_(urls), target_class.workspace_id == WorkspaceLookup.get_current_workspace_id()
        ).delete(synchronize_session=False)

    def get_urls(self, target_list: URLListType):
        if target_list == URLListType.BLOCKLIST:
            return self.blocklist_urls
        elif target_list == URLListType.BLOCKLIST_EXCEPTION:
            return self.blocklist_exception_urls
        elif target_list == URLListType.ALLOWLIST:
            return self.allowlist_urls
        elif target_list == URLListType.ALLOWLIST_EXCEPTION:
            return self.allowlist_exception_urls
