from Reservations.Domain.Models.Events import ReservationMade
from Reservations.Domain.ReadModels.Reservation.ReservationReadModel import ReservationReadModel
from Shared.Infrastructure_Abstractions.ContextRepository import ContextRepository


class ReservationDenormalizer:
    def __init__(self, context_repository: ContextRepository):
        self.context_repository = context_repository

    def Publish(self, event: ReservationMade):
        reservation_read_model = ReservationReadModel(event.__dict__)
        reservation_read_model.IsActive = True
        self.context_repository.Save(reservation_read_model)
