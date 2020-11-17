from typing import Dict, Callable, Type

from Reservations.Domain.Models import Events as events
from Reservations.Domain.ReadModels.Reservation.ReservationDenormalizer import ReservationDenormalizer

EVENT_HANDLERS = {
    events.ReservationMade: ReservationDenormalizer,
    events.ReservationRemoved: ReservationDenormalizer
}  # type:Dict[Type[events.Event], Callable]
