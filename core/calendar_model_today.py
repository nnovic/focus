from abc import abstractmethod

from core.abstract_model import AbstractModel
from core.calendar_event_descriptor import CalendarEventDescriptor


class CalendarModelToday(AbstractModel):
  

    @property
    def title(self) -> str:
        return "My day"
    
    @property
    def events(self) -> list[CalendarEventDescriptor]:
        events_list = self._get_events()
        return sorted(events_list, key=lambda event: event.start_time)


    @abstractmethod
    def _get_events(self) -> list[CalendarEventDescriptor]:
        raise NotImplementedError()
