from abc import abstractmethod

from core.abstract_model import AbstractModel
from core.bts_ticket_descriptor import BtsTicketDescriptor


class BtsModelMyActiveTickets(AbstractModel):

    @property
    def title(self) -> str:
        return "My active tickets"

    @property
    def tickets(self) -> list[BtsTicketDescriptor]:
        tickets_list = self._get_tickets()
        return sorted(tickets_list, key=lambda ticket: ticket.priority, reverse=True)

    @abstractmethod
    def _get_tickets(self) -> list[BtsTicketDescriptor]:
        raise NotImplementedError()
