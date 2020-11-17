import sys
import json
from flask import Flask, request

from Shared.CQRS_Essentials.Bus import Bus
from Reservations.Domain.Models import Commands
from Shared.CQRS_Essentials.Infrastructure.SqliteContextRepository import SqliteContextRepository
from Reservations.Domain.Models.Queries import FindReservationQuery
from ReservationApi.Handlers.HandlerMaps.CommandMap import COMMAND_HANDLERS
from ReservationApi.Handlers.HandlerMaps.EventMap import EVENT_HANDLERS
from ReservationApi.Handlers.HandlerMaps.QueryMap import QUERY_HANDLERS

app = Flask(__name__)
# in a dynamic language like Python, there is no need to use Dependency Injection to set our data repo.
# Normally this would be set by configuration, but for this exercise I've declared it directly
contextRepository = SqliteContextRepository()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/makereservation', methods=['POST'])
def make_reservation():
    try:
        bus = Bus(COMMAND_HANDLERS, EVENT_HANDLERS, QUERY_HANDLERS, contextRepository)
        cmd = Commands.MakeReservation(request.json['command'], request.json['rooms'])
        bus.handle(cmd)
        return f'OK. Room of type {cmd.RoomType} has been reserved', 200
    except Exception:
        e = sys.exc_info()
        return "Error occurred on room reservation. " + str(e[1]), 400


@app.route('/reservation/<string:hotel_id>/<string:reservation_id>', methods=['GET'])
def get_reservations(hotel_id: str, reservation_id: str):
    try:
        bus = Bus(COMMAND_HANDLERS, EVENT_HANDLERS, QUERY_HANDLERS, contextRepository)
        query = FindReservationQuery({"Id": reservation_id, "HotelId": hotel_id})
        read_model = bus.handle(query)
        return json.dumps(read_model.__dict__), 200
    except Exception:
        e = sys.exc_info()
        return "Error on reservation query " + str(e[1]), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
