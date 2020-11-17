from dataclasses import dataclass
import json

from Shared.CQRS_Essentials.CQRS.ReadModel import ReadModel

@dataclass
class ReservationReadModel(ReadModel):
    Id: str
    RoomType: str
    HotelId: str
    IsActive: bool

    def __init__(self, reservation_dictionary):
        json_text = json.dumps(reservation_dictionary)
        self.__dict__ = json.loads(json_text)
