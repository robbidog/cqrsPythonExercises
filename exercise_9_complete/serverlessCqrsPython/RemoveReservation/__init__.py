import logging
import sys
from os import path
sys.path.append(path.dirname(path.dirname(__file__)))

import azure.functions as func
from Shared.CQRS_Essentials.Bus import Bus
from Reservations.Domain.Models import Commands
from Shared.CQRS_Essentials.Infrastructure.SqliteContextRepository import SqliteContextRepository
from Reservations.Domain.Models.Queries import FindReservationQuery
from ReservationApi.Handlers.HandlerMaps.CommandMap import COMMAND_HANDLERS
from ReservationApi.Handlers.HandlerMaps.EventMap import EVENT_HANDLERS
from ReservationApi.Handlers.HandlerMaps.QueryMap import QUERY_HANDLERS

context_repository = SqliteContextRepository()
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        req_body = req.get_json()
        cmd = Commands.RemoveReservation(req_body)

        bus = Bus(COMMAND_HANDLERS, EVENT_HANDLERS, QUERY_HANDLERS, context_repository)
        bus.handle(cmd)
        return func.HttpResponse("Room Reservation Removed", status_code=200)
    except ValueError:
        e = sys.exc_info()
        return func.HttpResponse("Invalid data used in room reservation. " + str(e[1]), status_code=400)
    except Exception:
        e = sys.exc_info()
        return func.HttpResponse("Error occurred on room reservation. " + str(e[1]), status_code=400)