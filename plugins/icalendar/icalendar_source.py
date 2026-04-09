from typing import Any

from icalendar import Calendar
import requests

from core.data_source import DataSource
from plugins.icalendar.icalendar_models import IcalendarModelToday

class IcalendarSource(DataSource):

    def __init__(self):
        super().__init__()
        # self.__jira = None
        self.__config = None
        self.__today = IcalendarModelToday()
        self.__calendar = None

    def configure(self, config: Any):
        self.__config = config

    # @property
    # def __server(self):
    #     try:
    #         return self.__config.server
    #     except KeyError:
    #         return "https://atlassian.com"


    def _connect(self) -> None:
        pass
        # self.__jira = JIRA(
        #     server=self.__config.server,
        #     basic_auth=(self.__config.username, self.__config.token)
        # )
        # # Validate connection by fetching current user
        # try:
        #     self.__jira.current_user()
        # except Exception as e:
        #     raise ConnectionError(f"Failed to connect to Jira: {str(e)}")

    def _refresh(self) -> None:

        response = requests.get(self.__config.url, timeout=10)
        response.raise_for_status()

        self.__calendar = Calendar.from_ical(response.content)
        self.__refresh_today()

    def __refresh_today(self):
        self.__today._refresh(self.__calendar)

    def get_model(self, type: type) -> Any:
        # if type is BtsModelMyActiveTickets:
        #     return self.__active_tickets
        # else:
        #     raise NotImplementedError()
        raise NotImplementedError()
