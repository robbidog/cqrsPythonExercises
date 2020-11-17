import logging
import sys

# Azure Functions use a different import style from Standard Python see
# https://github.com/Azure/azure-functions-python-worker/issues/219 for an explanation
# The following two lines of code add the parent directory and all shared code
# to the python path and ensure that this path can be found after deployment without
# changing the import statements for other deployments that do not use Azure functions.
# The next two lines can be removed if you modify your PYTHONPATH environment variable
# to include the root directory of this project
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

contextRepository = SqliteContextRepository()


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        req_body = req.get_json()
        command_dictionary = req_body['command']
        room_dictionary = req_body['rooms']
        cmd = Commands.MakeReservation(command_dictionary, room_dictionary)

        bus = Bus(COMMAND_HANDLERS, EVENT_HANDLERS, QUERY_HANDLERS, contextRepository)
        bus.handle(cmd)
        return func.HttpResponse("Room Reserved", status_code=200)
    except ValueError:
        e = sys.exc_info()
        return func.HttpResponse("Invalid data used in room reservation. " + str(e[1]), status_code=400)
    except Exception:
        e = sys.exc_info()
        return func.HttpResponse("Error occurred on room reservation. " + str(e[1]), status_code=400)
