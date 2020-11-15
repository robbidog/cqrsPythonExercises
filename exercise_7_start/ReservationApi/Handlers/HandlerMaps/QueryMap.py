from typing import Dict, Callable, Type

from Reservations.Domain.Models import Queries as queries
from ReservationApi.Handlers.Query.ReservationsQueryHandler import ReservationQueryHandler

QUERY_HANDLERS = {
    queries.FindReservationQuery: ReservationQueryHandler
}  # type:Dict[Type[queries.Query], Callable]
