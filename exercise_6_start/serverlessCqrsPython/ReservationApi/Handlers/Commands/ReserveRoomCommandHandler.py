from Reservations.Domain.Models.Commands import MakeReservation
from Shared.CQRS_Essentials.EventStore.EventStoreClient import EventStoreClient
from Shared.CQRS_Essentials.Aggregates.AggregateFactory import AggregateFactory
from Shared.CQRS_Essentials.CQRS.ICommandHandler import ICommandHandler
from Reservations.Domain.Aggregates.Reservation import Reservation


class ReserveRoomCommandHandler(ICommandHandler):

    def __init__(self):
        self.factory = AggregateFactory()
        self.event_store_client = EventStoreClient()
        self.aggregate_type = type(Reservation())

    def Send(self, command: MakeReservation):
        reservation_id = command.Id
        reservation = self.factory.get(self.aggregate_type, reservation_id)
        events = reservation.Reserve(command)
        self.event_store_client.Save(reservation)
        return events
