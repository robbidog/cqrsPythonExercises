from Shared.CQRS_Essentials.CQRS.IQueryHandler import IQueryHandler
from Shared.CQRS_Essentials.CQRS.ReadModel import ReadModel
from Shared.CQRS_Essentials.CQRS.Query import Query
from Shared.Infrastructure_Abstractions.ContextRepository import ContextRepository
from Reservations.Domain.ReadModels.Reservation.ReservationReadModel import ReservationReadModel


class ReservationQueryHandler(IQueryHandler):
    def Handle(self, reservationQuery: Query):
        read_model = ReservationReadModel({"Id": "", "HotelId": "", "RoomType": "", "IsActive": False})

        return self.context_repository.Read(read_model, reservationQuery)

    def __init__(self, context_repository: ContextRepository):
        self.context_repository = context_repository
