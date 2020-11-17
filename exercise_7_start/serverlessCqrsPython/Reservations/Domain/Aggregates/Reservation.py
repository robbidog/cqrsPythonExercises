from dataclasses import dataclass
from ReservationApi.Services.Utilities import is_valid_uuid
from Reservations.Domain.Models.Commands import MakeReservation
from Reservations.Domain.Models.Events import ReservationMade
from Reservations.Domain.ReadModels.Reservation.ReservationReadModel import ReservationReadModel
from Shared.CQRS_Essentials.Aggregates.AggregateBase import AggregateBase
from Shared.CQRS_Essentials.Infrastructure.SqliteContextRepository import SqliteContextRepository


@dataclass
class _State:
    Id: str
    HotelId: str
    RoomType: str

    def __init__(self, command: MakeReservation = None):
        if command is None:
            self.Id = ""
            self.RoomType = ""
            self.HotelId = ""
        else:
            self.Id = command.Id
            self.RoomType = command.RoomType
            self.HotelId = command.HotelId


class Reservation(AggregateBase):
    def __init__(self):
        self.State = _State()
        self.applied_events = [type(ReservationMade()).__name__]
        self.contextRepository = SqliteContextRepository()  # todo this should be passed in as a parameter or from a config file, not hard coded
        self.blank_reservation_read_model = ReservationReadModel({"Id": "", "HotelId": "", "RoomType": "", "IsActive": False})

    def Reserve(self, command: MakeReservation):
        if not is_valid_uuid(command.HotelId):
            raise ValueError(command.HotelId, 'Hotel Id must be a valid uuid')
        if not is_valid_uuid(command.Id):
            raise ValueError(command.Id, 'Room Id must be a valid uuid')
        sql_stmt = "select count(*) as room_count from " + type(
            self.blank_reservation_read_model).__name__ + f" where RoomType='{command.RoomType}' and HotelId='{command.HotelId}' and IsActive='True'"
        results = self.contextRepository.ReadQuery(self.blank_reservation_read_model, sql_stmt)
        if results is not None:
            room_count = results[0]['room_count']
            if room_count >= command.RoomInventory[command.RoomType]:
                raise Exception("No available rooms of type " + command.RoomType)
        self.State = _State(command)
        event = ReservationMade(Id=command.Id, RoomType=command.RoomType, HotelId=command.HotelId)
        self.uncommitted_events.append(event)
        return self.uncommitted_events

    #
    # I feel safe referencing the elements of the event_data by name as any type of Reservation Command will always require
    # Room, Hotel and a reservation Id.  If any is not present than an exception must be thrown
    def apply(self, event_data: dict):
        self.State.Id = event_data['Id']
        self.State.HotelId = event_data['HotelId']
        self.State.RoomType = event_data['RoomType']
