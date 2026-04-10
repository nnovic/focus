from datetime import datetime


class CalendarEventDescriptor:
    
    @property
    def summary(self) -> str:
        raise NotImplementedError()

    @property
    def start_time(self) -> datetime:
        raise NotImplementedError()
    
    @property
    def end_time(self) -> datetime:
        raise NotImplementedError()
    
    @property
    def duration(self) -> float|None:
        return None
    
    # def __init__(self, summary: str, start: datetime, end: datetime = None, location: str = ""):
    #     self.title = summary
    #     self.start_time = start
    #     self.end_time = end
    #     self.location = location
    #     self.is_all_day = isinstance(start, str)  # Simple check for all-day events

    # def __repr__(self) -> str:
    #     return f"CalendarEntry(title='{self.title}', start={self.start_time})"
