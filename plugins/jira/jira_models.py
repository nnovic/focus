from typing import Any
from datetime import datetime

from core.bts_model_my_active_tickets import BtsModelMyActiveTickets
from core.bts_ticket_descriptor import BtsTicketDescriptor


class JiraTicketDescriptor(BtsTicketDescriptor):
    def __init__(self, issue):
        super().__init__()
        self.__issue = issue

    @property
    def uuid(self) -> Any:
        return self.__issue.id
    
    @property
    def title(self) -> str:
        return f"{self.__issue.key} {self.__issue.fields.summary}"

    @property
    def url(self) -> str | None:
        return self.__issue.permalink()

    @property
    def created_at(self) -> datetime | None:
        # Handle timezone offset formatting (e.g., '+0100' -> '+01:00')
        created_str = self.__issue.fields.created
        if created_str and len(created_str) > 6:
            # Insert colon in timezone offset if missing (last 5 chars)
            if created_str[-5] in ('+', '-') and ':' not in created_str[-5:]:
                created_str = created_str[:-2] + ':' + created_str[-2:]
        return datetime.fromisoformat(created_str)

    @property
    def priority(self) -> int:
    #     """Return priority based on Jira priority field."""
    #     priority_map = {
    #         "Highest": 100,
    #         "High": 80,
    #         "Medium": 60,
    #         "Low": 40,
    #         "Lowest": 20,
    #     }
    #     priority_name = self.__issue.fields.priority.name if self.__issue.fields.priority else "Medium"
    #    return priority_map.get(priority_name, 50)
        return self.__issue.fields.priority


class JiraModelMyActiveTickets(BtsModelMyActiveTickets):
    def __init__(self):
        self.__list = []

    @property
    def title(self) -> str:
        return "My Issues @Jira"

    def _refresh(self, jira_client):
        # Query for issues assigned to current user that are not done and in an active sprint
        jql = 'assignee = currentUser() AND resolution = UNRESOLVED AND sprint in openSprints()'
        issues = jira_client.search_issues(jql, maxResults=False)

        new_list = []
        for issue in issues:
            desc = JiraTicketDescriptor(issue)
            new_list.append(desc)

        self.__list = new_list

    # def _get_pull_requests(self) -> list[GenericTaskDescriptor]:
    #     return self.__list


    def _get_tickets(self) -> list[BtsTicketDescriptor]:
        return self.__list