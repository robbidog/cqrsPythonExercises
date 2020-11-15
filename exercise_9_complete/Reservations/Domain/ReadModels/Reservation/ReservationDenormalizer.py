from Shared.CQRS_Essentials.CQRS.Event import Event
from Reservations.Domain.Models.Events import ReservationMade, ReservationRemoved
from Reservations.Domain.ReadModels.Reservation.ReservationReadModel import ReservationReadModel
from Shared.Infrastructure_Abstractions.ContextRepository import ContextRepository


class ReservationDenormalizer:
    def __init__(self, context_repository: ContextRepository):
        self.context_repository = context_repository

    def Publish(self, event: Event):
        reservation_read_model = ReservationReadModel(event.__dict__)
        if isinstance(event, ReservationMade):
            reservation_read_model.IsActive = True
        elif isinstance(event, ReservationRemoved):
            reservation_read_model.IsActive = False
        else:
            raise ValueError(f'Improper event of type {type(event)} sent to reservation denormalizer')

        self.context_repository.Save(reservation_read_model)


