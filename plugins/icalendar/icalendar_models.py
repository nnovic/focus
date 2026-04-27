# from typing import Any
from datetime import datetime, timedelta
import math
from dateutil.rrule import rrulestr


from core.calendar_event_descriptor import CalendarEventDescriptor
from core.calendar_model_today import CalendarModelToday


def _round_date(dt) -> datetime:
    return datetime.combine(dt, datetime.min.time())


class IcalendarEventDescriptor(CalendarEventDescriptor):
    def __init__(self, component):
        self.__component = component

    @property
    def summary(self) -> str:
        summary = self.__component.get("summary", "")
        return str(summary)

    @property
    def start_time(self) -> datetime:
        dtstart = self.__component.get("dtstart")
        start_dt = dtstart.dt
        if hasattr(start_dt, 'date'):
            start_date_obj = start_dt if isinstance(
                start_dt, datetime) else _round_date(start_dt)
        else:
            start_date_obj = _round_date(start_dt)
        return start_date_obj

    @property
    def end_time(self) -> datetime:
        dtend = self.__component.get("dtend")
        end_dt = dtend.dt
        if hasattr(end_dt, 'date'):
            end_date_obj = end_dt if isinstance(
                end_dt, datetime) else _round_date(end_dt)
        else:
            end_date_obj = _round_date(end_dt)
        return end_date_obj

    @property
    def __is_all_day(self) -> bool:
        return False

    @property
    def duration(self) -> float | None:
        if self.__is_all_day:
            return math.inf
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 3600

    @property
    def location(self) -> str | None:
        loc = self.__component.get("location", "")
        return str(loc) if loc else None

    @property
    def url(self) -> str | None:
        url = self.__component.get("url", "")
        return str(url) if url else None


class IcalendarOccurrenceDescriptor(IcalendarEventDescriptor):
    """Wraps a recurring event component with a specific occurrence's start/end times."""

    def __init__(self, component, occurrence_start: datetime, occurrence_end: datetime):
        super().__init__(component)
        self.__occurrence_start = occurrence_start
        self.__occurrence_end = occurrence_end

    @property
    def start_time(self) -> datetime:
        return self.__occurrence_start

    @property
    def end_time(self) -> datetime:
        return self.__occurrence_end


def _expand_recurrences(component, start_date: datetime, end_date: datetime) -> list[IcalendarOccurrenceDescriptor]:
    dtstart = component.get("dtstart").dt
    if not isinstance(dtstart, datetime):
        dtstart = datetime.combine(dtstart, datetime.min.time())
    dtstart = dtstart.replace(tzinfo=None)

    dtend = component.get("dtend")
    if dtend:
        end_dt = dtend.dt
        if not isinstance(end_dt, datetime):
            end_dt = datetime.combine(end_dt, datetime.min.time())
        duration = end_dt.replace(tzinfo=None) - dtstart
    else:
        duration = timedelta(0)

    rrule_str = "RRULE:" + component.get("rrule").to_ical().decode()
    rule = rrulestr(rrule_str, dtstart=dtstart, ignoretz=True)

    search_start = datetime.combine(start_date.date(), datetime.min.time())
    search_end = datetime.combine(end_date.date(), datetime.max.time())

    return [
        IcalendarOccurrenceDescriptor(component, occ, occ + duration)
        for occ in rule.between(search_start, search_end, inc=True)
    ]


def _get_events_range(calendar, start_date: datetime, end_date: datetime) -> list[CalendarEventDescriptor]:
    """
    Retrieve calendar events for a date range.

    Args:
        start_date: Start date for the range
        end_date: End date for the range

    Returns:
        List of CalendarEntry objects in the date range
    """

    if not calendar:
        raise RuntimeError("Calendar not loaded. Call connect() first.")

    events = []
    for component in calendar.walk():
        if component.name == "VEVENT":
            # dtstart = component.get("dtstart")
            # dtend = component.get("dtend")
            # summary = component.get("summary", "")
            # location = component.get("location", "")

            if component.get("rrule"):
                events.extend(_expand_recurrences(
                    component, start_date, end_date))
            else:
                event = IcalendarEventDescriptor(component)
                if event.start_time.date() >= start_date.date() and event.start_time.date() <= end_date.date():
                    events.append(event)
                elif event.start_time.date() < start_date.date() and event.end_time.date() >= start_date.date():
                    events.append(event)
        else:
            pass

    return events


class IcalendarModelToday(CalendarModelToday):
    def __init__(self):
        self.__list = []

    @property
    def title(self) -> str:
        return "My ICalendar day"

    def _refresh(self, ical):

        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time())
        today_end = datetime.combine(today, datetime.max.time())

        self.__list = _get_events_range(ical, today_start, today_end)
        pass

    def _get_events(self) -> list[CalendarEventDescriptor]:
        return self.__list
