import json
from dataclasses import dataclass
from Shared.CQRS_Essentials.CQRS.Query import Query


@dataclass
class FindReservationQuery(Query):
    HotelId: str
    Id: str

    def __init__(self, query_dictionary):
        json_text = json.dumps(query_dictionary)
        self.__dict__ = json.loads(json_text)