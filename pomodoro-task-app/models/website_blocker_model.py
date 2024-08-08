from contextlib import contextmanager

from PySide6.QtCore import QObject
from enum import Enum
from models.workspace_list_model import workplace_model
from sqlalchemy.orm import sessionmaker
from models.db_tables import engine, Workspace
from constants import WebsiteFilterType, URLListType
from models.db_tables import BlocklistURL, BlocklistExceptionURL, AllowlistURL, AllowlistExceptionURL
from urllib.parse import urlparse
from loguru import logger
import re


@contextmanager
def get_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

class WebsiteBlockerModel(QObject):
    def __init__(self):
        super().__init__()

        self.blocklist_urls = []
        self.blocklist_exception_urls = []
        self.allowlist_urls = []
        self.allowlist_exception_urls = []

        self.workplace_model = workplace_model
        self.website_filter_type = None

        self.load_data()

    def load_data(self, target_list: URLListType = None):
        with get_session() as session:
            current_workspace_id = self.workplace_model.get_current_workspace_id()

            if target_list == None:
                self.blocklist_urls = [url.url for url in session.query(BlocklistURL).filter(BlocklistURL.workspace_id == current_workspace_id).all()]
                self.blocklist_exception_urls = [url.url for url in session.query(BlocklistExceptionURL).filter(BlocklistExceptionURL.workspace_id == current_workspace_id).all()]
                self.allowlist_urls = [url.url for url in session.query(AllowlistURL).filter(AllowlistURL.workspace_id == current_workspace_id).all()]
                self.allowlist_exception_urls = [url.url for url in session.query(AllowlistExceptionURL).filter(AllowlistExceptionURL.workspace_id == current_workspace_id).all()]
            elif target_list == URLListType.BLOCKLIST:
                self.blocklist_urls = [url.url for url in session.query(BlocklistURL).filter(BlocklistURL.workspace_id == current_workspace_id).all()]
            elif target_list == URLListType.BLOCKLIST_EXCEPTION:
                self.blocklist_exception_urls = [url.url for url in session.query(BlocklistExceptionURL).filter(BlocklistExceptionURL.workspace_id == current_workspace_id).all()]
            elif target_list == URLListType.ALLOWLIST:
                self.allowlist_urls = [url.url for url in session.query(AllowlistURL).filter(AllowlistURL.workspace_id == current_workspace_id).all()]
            elif target_list == URLListType.ALLOWLIST_EXCEPTION:
                self.allowlist_exception_urls = [url.url for url in session.query(AllowlistExceptionURL).filter(AllowlistExceptionURL.workspace_id == current_workspace_id).all()]

    def set_website_filter_type(self, website_filter_type: WebsiteFilterType):
        with get_session() as session:
            current_workspace_id = self.workplace_model.get_current_workspace_id()
            current_workspace = session.query(Workspace).filter(Workspace.id == current_workspace_id).first()
            current_workspace.website_filter_type = website_filter_type
            session.add(current_workspace)
            self.website_filter_type = website_filter_type

    def get_website_filter_type(self):
        return self.website_filter_type

    def update_target_list_urls(self, target_list: URLListType, target_list_urls: list):  # todo: find out how to pass the urls as a list
        valid_urls = []
        for line_number, url in enumerate(target_list_urls):
            result = self.validate_url(url)
            if not result:
                logger.error(f"Invalid URL at line {line_number + 1}: {url}")
            else:
                valid_urls.append(url)

        valid_urls_set = set(valid_urls)  # remove duplicates

        with get_session() as session:

            current_urls_set = set()
            target_class = None

            if target_list == URLListType.BLOCKLIST:
                current_urls_set = set(self.blocklist_urls)
                target_class = BlocklistURL
            elif target_list == URLListType.BLOCKLIST_EXCEPTION:
                current_urls_set = set(self.blocklist_exception_urls)
                target_class = BlocklistExceptionURL
            elif target_list == URLListType.ALLOWLIST:
                current_urls_set = set(self.allowlist_urls)
                target_class = AllowlistURL
            elif target_list == URLListType.ALLOWLIST_EXCEPTION:
                current_urls_set = set(self.allowlist_exception_urls)
                target_class = AllowlistExceptionURL

            urls_to_add = valid_urls_set - current_urls_set  # new url = url not in old set but in new set
            urls_to_remove = current_urls_set - valid_urls_set # removed url = url not in new set but in old set

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
    def add_urls(self, session, urls, target_class):
        for url in urls:
            session.add(target_class(workspace_id=self.workplace_model.get_current_workspace_id(), url=url))

    # helper function for update_target_list_urls()
    def remove_urls(self, session, urls, target_class):
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