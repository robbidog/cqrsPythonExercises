from typing import Dict, Callable, Type

from Reservations.Domain.Models import Commands as commands
from ReservationApi.Handlers.Commands.ReserveRoomCommandHandler import ReserveRoomCommandHandler


COMMAND_HANDLERS = {
        commands.MakeReservation: ReserveRoomCommandHandler,
    }  # type: Dict[Type[commands.Command], Callable]
