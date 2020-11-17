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

@dataclass
class ReservationRemoved(Event):
    Id: str
    RoomType: str
    HotelId: str

    def __init__(self, Id: str = None, RoomType: str = None, HotelId: str = None):
        self.Id = Id
        self.RoomType = RoomType
        self.HotelId = HotelId

if __name__ == '__main__':
    import uuid
    import json
    reservation_dictionary = {'Id': str(uuid.uuid4()),
                              'RoomType': 'Presidential',
                              'HotelId': str(uuid.uuid4())}
    room_id = str(uuid.uuid4())
    room_type = 'Presidential'
    hotel_id = str(uuid.uuid4())
    reserveCommand = ReservationMade(room_id, room_type, hotel_id)
    print(json.dumps(reserveCommand.__dict__))
    remove_reservation_command = ReservationRemoved(room_id, room_type, hotel_id)
    print(json.dumps(remove_reservation_command.__dict__))