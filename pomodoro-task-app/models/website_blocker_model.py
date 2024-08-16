from contextlib import contextmanager

from PySide6.QtCore import QObject
from enum import Enum
from models.workspace_list_model import WorkspaceListModel
from models.db_tables import engine, Workspace
from constants import WebsiteFilterType, URLListType
from models.db_tables import BlocklistURL, BlocklistExceptionURL, AllowlistURL, AllowlistExceptionURL
from utils.db_utils import get_session
from urllib.parse import urlparse
from loguru import logger
from models.workspace_lookup import WorkspaceLookup
import re


class WebsiteBlockerModel(QObject):
    def __init__(self):
        super().__init__()

        self.blocklist_urls = set()
        self.blocklist_exception_urls = set()
        self.allowlist_urls = set()
        self.allowlist_exception_urls = set()

        self.website_filter_type = None

        self.load_data()

    def load_data(self, target_list: URLListType = None):
        with get_session(is_read_only=True) as session:
            current_workspace_id = WorkspaceLookup.get_current_workspace_id()

            if target_list == None:
                self.blocklist_urls = {url.url for url in session.query(BlocklistURL).filter(BlocklistURL.workspace_id == current_workspace_id).all()}
                self.blocklist_exception_urls = {url.url for url in session.query(BlocklistExceptionURL).filter(BlocklistExceptionURL.workspace_id == current_workspace_id).all()}
                self.allowlist_urls = {url.url for url in session.query(AllowlistURL).filter(AllowlistURL.workspace_id == current_workspace_id).all()}
                self.allowlist_exception_urls = {url.url for url in session.query(AllowlistExceptionURL).filter(AllowlistExceptionURL.workspace_id == current_workspace_id).all()}
            elif target_list == URLListType.BLOCKLIST:
                self.blocklist_urls = {url.url for url in session.query(BlocklistURL).filter(BlocklistURL.workspace_id == current_workspace_id).all()}
                logger.debug(f"Inside if condition of load_data() for BLOCKLIST")
            elif target_list == URLListType.BLOCKLIST_EXCEPTION:
                self.blocklist_exception_urls = {url.url for url in session.query(BlocklistExceptionURL).filter(BlocklistExceptionURL.workspace_id == current_workspace_id).all()}
            elif target_list == URLListType.ALLOWLIST:
                self.allowlist_urls = {url.url for url in session.query(AllowlistURL).filter(AllowlistURL.workspace_id == current_workspace_id).all()}
            elif target_list == URLListType.ALLOWLIST_EXCEPTION:
                self.allowlist_exception_urls = {url.url for url in session.query(AllowlistExceptionURL).filter(AllowlistExceptionURL.workspace_id == current_workspace_id).all()}

    def set_website_filter_type(self, website_filter_type: WebsiteFilterType):
        with get_session() as session:
            current_workspace = WorkspaceLookup.get_current_workspace()
            current_workspace.website_filter_type = website_filter_type
            session.add(current_workspace)
            self.website_filter_type = website_filter_type

    def get_website_filter_type(self):
        return self.website_filter_type

    def update_target_list_urls(self, target_list: URLListType, target_list_urls: set):
        valid_urls = set()
        for line_number, url in enumerate(target_list_urls):
            result = self.validate_url(url)
            if not result:
                # todo: show error message in UI
                logger.error(f"Invalid URL at line {line_number + 1}: {url}")
            else:
                valid_urls.add(url)

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


            urls_to_add = valid_urls - current_urls  # new url = url not in old set but in new set
            urls_to_remove = current_urls - valid_urls # removed url = url not in new set but in old set

            if urls_to_remove:
                self.remove_urls(session, urls_to_remove, target_class)

            if urls_to_add:
                self.add_urls(session, urls_to_add, target_class)

            self.load_data(target_list)

    # helper function for validate_url()
    def add_default_scheme(self, url):
        if not urlparse(url).scheme:
            return f"https://{url}"

    # helper function for is_valid_url()
    def is_valid_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    # helper function for is_valid_url()
    def is_valid_domain(self, domain):
        regex = r'^(?!:\/\/)([a-zA-Z0-9-_]+\.)*[a-zA-Z0-9][a-zA-Z0-9-_]+\.[a-zA-Z]{2,11}?$'
        return re.match(regex, domain) is not None

    def validate_url(self, url):
        url = self.add_default_scheme(url)
        if not self.is_valid_url(url):
            return False

        parsed_url = urlparse(url)
        result = self.is_valid_domain(parsed_url.netloc)

        if result:
            return (result, url)
        else:
            return (result, None)

    # helper function for update_target_list_urls()
    def add_urls(self, session, urls: set, target_class):
        for url in urls:
            session.add(target_class(workspace_id=WorkspaceLookup.get_current_workspace_id(), url=url))

    # helper function for update_target_list_urls()
    def remove_urls(self, session, urls: set, target_class):
        session.query(target_class).filter(target_class.url.in_(urls)).delete(synchronize_session=False)

    def get_urls(self, target_list: URLListType):
        if target_list == URLListType.BLOCKLIST:
            return self.blocklist_urls
        elif target_list == URLListType.BLOCKLIST_EXCEPTION:
            return self.blocklist_exception_urls
        elif target_list == URLListType.ALLOWLIST:
            return self.allowlist_urls
        elif target_list == URLListType.ALLOWLIST_EXCEPTION:
            return self.allowlist_exception_urls
