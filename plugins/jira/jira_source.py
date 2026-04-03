from typing import Any

from core.data_source import DataSource
from jira import JIRA

from plugins.jira.jira_models import *


class JiraSource(DataSource):

    def __init__(self):
        super().__init__()
        self.__jira = None
        self.__config = None
        self.__active_tickets = JiraModelMyActiveTickets()

    def configure(self, config: Any):
        self.__config = config

    def _connect(self) -> None:
        self.__jira = JIRA(
            server=self.__config.server,
            basic_auth=(self.__config.username, self.__config.token)
        )
        # Validate connection by fetching current user
        try:
            self.__jira.current_user()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Jira: {str(e)}")

    def _refresh(self) -> None:
        self.__refresh_my_tickets_in_active_sprints()

    def __refresh_my_tickets_in_active_sprints(self):
        self.__active_tickets._refresh(self.__jira)

    def get_model(self, type: type) -> Any:
        if type is BtsModelMyActiveTickets:
            return self.__active_tickets
        else:
            raise NotImplementedError()
