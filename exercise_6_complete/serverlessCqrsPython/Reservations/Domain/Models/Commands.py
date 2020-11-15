from dataclasses import dataclass
import json
import uuid

from Shared.CQRS_Essentials.CQRS.Command import Command


@dataclass
class MakeReservation(Command):
    Id: str
    RoomType: str
    HotelId: str
    RoomInventory: dict

    def __init__(self, reserve_dictionary: dict, inventory: dict):
        json_text = json.dumps(reserve_dictionary)
        self.__dict__ = json.loads(json_text)
        self.RoomInventory = inventory

@dataclass
class RemoveReservation(Command):
    Id: str
    RoomType: str
    HotelId: str

    def __init__(self, reserve_dictionary: dict):
        json_text = json.dumps(reserve_dictionary)
        self.__dict__ = json.loads(json_text)

if __name__ == '__main__':
    reservation_dictionary = {'Id': str(uuid.uuid4()),
                              'RoomType': 'Presidential',
                              'HotelId': str(uuid.uuid4())}
    reserveCommand = MakeReservation(reservation_dictionary, {'Presidential': 1, "Suites": 5})
    print(json.dumps(reserveCommand.__dict__))
    remove_reservation_command = RemoveReservation(reservation_dictionary)
    print(json.dumps(remove_reservation_command.__dict__))
