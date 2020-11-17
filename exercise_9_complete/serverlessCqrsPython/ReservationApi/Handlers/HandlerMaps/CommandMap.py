from typing import Dict, Callable, Type

from Reservations.Domain.Models import Commands as commands
from ReservationApi.Handlers.Commands.ReserveRoomCommandHandler import ReserveRoomCommandHandler
from ReservationApi.Handlers.Commands.RemoveReservationCommandHandler import RemoveReservationCommandHandler


COMMAND_HANDLERS = {
        commands.MakeReservation: ReserveRoomCommandHandler,
        commands.RemoveReservation: RemoveReservationCommandHandler
    }  # type: Dict[Type[commands.Command], Callable]
