from datetime import datetime, timedelta
from typing import List, Dict, Any
from exchangelib import Account, Configuration, Credentials, EWSDateTime
from exchangelib.items import CalendarItem


class OutlookCalendarEntry:
    """Represents a calendar entry from Outlook."""

    def __init__(self, calendar_item: CalendarItem):
        self.title = calendar_item.subject
        self.start_time = calendar_item.start
        self.end_time = calendar_item.end
        self.location = calendar_item.location if hasattr(calendar_item, 'location') else ""
        self.is_all_day = calendar_item.is_all_day
        self.organizer = calendar_item.organizer if hasattr(calendar_item, 'organizer') else ""

    def __repr__(self) -> str:
        return f"OutlookCalendarEntry(title='{self.title}', start={self.start_time})"


class OutlookCalendar:
    """Manages connection to Outlook calendar and retrieves calendar entries."""

    def __init__(self, email: str, password: str):
        """
        Initialize Outlook calendar connection.

        Args:
            email: Outlook/Microsoft 365 email address
            password: Email account password
        """
        self.email = email
        self.password = password
        self.account = None

    def connect(self) -> bool:
        """
        Connect to Outlook account using basic authentication (EWS).

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            credentials = Credentials(self.email, self.password)
            config = Configuration(server='outlook.office365.com', credentials=credentials)
            self.account = Account(
                primary_smtp_address=self.email,
                config=config,
                autodiscover=False
            )
            # Test the connection
            _ = self.account.inbox.all().count()
            return True
        except Exception as e:
            print(f"Failed to connect to Outlook: {e}")
            return False

    def get_today_events(self) -> List[OutlookCalendarEntry]:
        """
        Retrieve all calendar events for today.

        Returns:
            List of OutlookCalendarEntry objects for today
        """
        if not self.account:
            raise RuntimeError("Not connected to Outlook. Call connect() first.")

        try:
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1)

            events = self.account.calendar.filter(
                start__gte=today_start,
                start__lt=today_end
            ).order_by('start')

            return [OutlookCalendarEntry(event) for event in events]
        except Exception as e:
            print(f"Failed to retrieve calendar events: {e}")
            return []

    def get_events_range(self, start_date: datetime, end_date: datetime) -> List[OutlookCalendarEntry]:
        """
        Retrieve calendar events for a date range.

        Args:
            start_date: Start date for the range
            end_date: End date for the range

        Returns:
            List of OutlookCalendarEntry objects in the date range
        """
        if not self.account:
            raise RuntimeError("Not connected to Outlook. Call connect() first.")

        try:
            events = self.account.calendar.filter(
                start__gte=start_date,
                start__lt=end_date
            ).order_by('start')

            return [OutlookCalendarEntry(event) for event in events]
        except Exception as e:
            print(f"Failed to retrieve calendar events: {e}")
            return []
