from abc import abstractmethod
from datetime import datetime

from core.abstract_model import AbstractModel
from core.calendar_event_descriptor import CalendarEventDescriptor


class CalendarModelToday(AbstractModel):


    @property
    def title(self) -> str:
        return "My day"

    @property
    def events(self) -> list[CalendarEventDescriptor]:
        events_list = self._get_events()
        return sorted(events_list, key=lambda event: self._normalize_datetime(event.start_time))

    @staticmethod
    def _normalize_datetime(dt: datetime) -> datetime:
        """Normalize datetime to be naive (remove timezone info) for comparison."""
        if dt.tzinfo is not None:
            return dt.replace(tzinfo=None)
        return dt

    @abstractmethod
    def _get_events(self) -> list[CalendarEventDescriptor]:
        raise NotImplementedError()
