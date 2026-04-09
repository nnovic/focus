from datetime import datetime
from typing import List
import xml.etree.ElementTree as ET
import requests
from icalendar import Calendar


class CalendarEntry:
    """Represents a calendar entry."""

    def __init__(self, summary: str, start: datetime, end: datetime = None, location: str = ""):
        self.title = summary
        self.start_time = start
        self.end_time = end
        self.location = location
        self.is_all_day = isinstance(start, str)  # Simple check for all-day events

    def __repr__(self) -> str:
        return f"CalendarEntry(title='{self.title}', start={self.start_time})"


class SharedOutlookCalendar:
    """Manages access to shared Outlook calendar via iCalendar URL."""

    def __init__(self, ical_url: str):
        """
        Initialize calendar with iCalendar URL.

        Args:
            ical_url: URL to the iCalendar (.ics) file
        """
        self.ical_url = ical_url
        self.calendar = None

    def connect(self) -> bool:
        """
        Download and parse the calendar from the iCalendar URL.

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            response = requests.get(self.ical_url, timeout=10)
            response.raise_for_status()

            self.calendar = Calendar.from_ical(response.content)
            print(f"Successfully loaded calendar from {self.ical_url}")
            return True
        except Exception as e:
            print(f"Failed to load calendar: {e}")
            return False

    def get_today_events(self) -> List[CalendarEntry]:
        """
        Retrieve all calendar events for today.

        Returns:
            List of CalendarEntry objects for today
        """
        if not self.calendar:
            raise RuntimeError("Calendar not loaded. Call connect() first.")

        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time())
        today_end = datetime.combine(today, datetime.max.time())

        return self.get_events_range(today_start, today_end)

    def get_events_range(self, start_date: datetime, end_date: datetime) -> List[CalendarEntry]:
        """
        Retrieve calendar events for a date range.

        Args:
            start_date: Start date for the range
            end_date: End date for the range

        Returns:
            List of CalendarEntry objects in the date range
        """
        if not self.calendar:
            raise RuntimeError("Calendar not loaded. Call connect() first.")

        try:
            events = []
            for component in self.calendar.walk():
                if component.name == "VEVENT":
                    dtstart = component.get("dtstart")
                    dtend = component.get("dtend")
                    summary = component.get("summary", "")
                    location = component.get("location", "")

                    if dtstart:
                        # Handle both datetime and date objects
                        start_dt = dtstart.dt
                        if hasattr(start_dt, 'date'):
                            start_date_obj = start_dt if isinstance(start_dt, datetime) else datetime.combine(start_dt, datetime.min.time())
                        else:
                            start_date_obj = datetime.combine(start_dt, datetime.min.time())

                        # Check if event is in the requested range
                        if start_date_obj.date() >= start_date.date() and start_date_obj.date() <= end_date.date():
                            end_dt = dtend.dt if dtend else start_date_obj
                            if not hasattr(end_dt, 'time'):
                                end_dt = datetime.combine(end_dt, datetime.max.time())

                            events.append(CalendarEntry(
                                summary=str(summary),
                                start=start_date_obj,
                                end=end_dt,
                                location=str(location)
                            ))

            # Sort by start time
            events.sort(key=lambda e: e.start_time)
            return events
        except Exception as e:
            print(f"Failed to retrieve calendar events: {e}")
            return []


def parse_sharing_message_xml(xml_content: str) -> str:
    """
    Parse the sharing message XML and extract the iCalendar URL.

    Args:
        xml_content: The XML content as a string

    Returns:
        str: The iCalendar URL or None if not found
    """
    try:
        root = ET.fromstring(xml_content)
        # Define namespace
        ns = {'ex': 'http://schemas.microsoft.com/exchange/sharing/2008'}

        # Find the ICalUrl element
        ical_url_elem = root.find('.//ex:ICalUrl', ns)
        if ical_url_elem is not None:
            return ical_url_elem.text
        return None
    except Exception as e:
        print(f"Failed to parse XML: {e}")
        return None


def test_shared_calendar():
    # Example XML parsing
    xml_content = """<SharingMessage xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.microsoft.com/sharing/2008">
<DataType>calendar</DataType>
<Initiator>
<Name>Alexandre VINCON</Name>
<SmtpAddress>avincon@groupe-atlantic.com</SmtpAddress>
</Initiator>
<Invitation>
<Providers>
<Provider Type="ms-exchange-publish" TargetRecipients="nnovic@yahoo.fr">
<BrowseUrl xmlns="http://schemas.microsoft.com/exchange/sharing/2008">https://outlook.office365.com/owa/calendar/09247b53ef2440b59e84915f7335036c@groupe-atlantic.com/cc599fb200bf4d29970952b3ec778c3a821442519967883327/S-1-8-672916694-197202260-2267550140-356204824/reachcalendar.html</BrowseUrl>
<ICalUrl xmlns="http://schemas.microsoft.com/exchange/sharing/2008">https://outlook.office365.com/owa/calendar/09247b53ef2440b59e84915f7335036c@groupe-atlantic.com/cc599fb200bf4d29970952b3ec778c3a821442519967883327/S-1-8-672916694-197202260-2267550140-356204824/reachcalendar.ics</ICalUrl>
</Provider>
</Providers>
</Invitation>
</SharingMessage>"""

    # Parse XML to get iCalendar URL
    ical_url = parse_sharing_message_xml(xml_content)
    if not ical_url:
        print("Failed to extract iCalendar URL from XML")
        return

    print(f"Found iCalendar URL: {ical_url}")

    # Load and retrieve calendar events
    calendar = SharedOutlookCalendar(ical_url)
    if calendar.connect():
        events = calendar.get_today_events()
        print(f"\nFound {len(events)} events for today:")
        for event in events:
            print(f"  - {event.title} at {event.start_time}")
            if event.location:
                print(f"    Location: {event.location}")
    else:
        print("Failed to load calendar")


if __name__ == "__main__":
    test_shared_calendar()
