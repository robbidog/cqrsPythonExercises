from Reservations.Domain.Models.Commands import RemoveReservation
from Shared.CQRS_Essentials.EventStore.EventStoreClient import EventStoreClient
from Shared.CQRS_Essentials.Aggregates.AggregateFactory import AggregateFactory
from Shared.CQRS_Essentials.CQRS.CommandHandler import CommandHandler
from Reservations.Domain.Aggregates.Reservation import Reservation


class RemoveReservationCommandHandler(CommandHandler):

    def __init__(self):
        self.factory = AggregateFactory()
        self.event_store_client = EventStoreClient()
        self.aggregate_type = type(Reservation())

    def Publish(self, command: RemoveReservation):
        reservation_id = command.Id
        reservation = self.factory.get(self.aggregate_type, reservation_id)
        # todo complete exercise 7 and implement this command in the next exercise
        # events = reservation.RemoveReservation(command)
        self.event_store_client.Save(reservation)
        # return events
