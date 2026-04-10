from typing import Any

from icalendar import Calendar
import requests

from core.calendar_model_today import CalendarModelToday
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

    def _disconnect(self) -> None:
        pass

    def _refresh(self) -> None:

        response = requests.get(self.__config.url, timeout=10)
        response.raise_for_status()

        self.__calendar = Calendar.from_ical(response.content)
        self.__refresh_today()

    def __refresh_today(self):
        self.__today._refresh(self.__calendar)

    def get_model(self, type: type) -> Any:
        if type is CalendarModelToday:
            return self.__today
        else:
            raise NotImplementedError()
