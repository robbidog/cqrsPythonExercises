import uuid

from Reservations.Domain.Models.Events import ReservationMade


def is_valid_uuid(val: str):
    try:
        if val == '00000000-0000-0000-0000-000000000000':
            return False
        guid = uuid.UUID(val, version=4)
        if int(guid.hex, 16) > 0:
            return True
        return False
    except ValueError:
        return False
