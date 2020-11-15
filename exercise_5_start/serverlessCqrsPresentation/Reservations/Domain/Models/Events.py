from dataclasses import dataclass
from Shared.CQRS_Essentials.CQRS.Event import Event


@dataclass
class ReservationMade(Event):
    Id: str
    RoomType: str
    HotelId: str

    def __init__(self, Id: str = None, RoomType: str = None, HotelId: str = None):
        self.Id = Id
        self.RoomType = RoomType
        self.HotelId = HotelId
