import asyncio
import uuid
import os
import json

import photonpump

from Shared.CQRS_Essentials.Aggregates.AggregateBase import AggregateBase


class EventStoreClient:

    def __init__(self):
        self.config = {}
        current_directory = os.getcwd()
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)
        with open('../../../ReservationApi/config.json', 'r') as f:
            self.config = json.load(f)

        os.chdir(current_directory)

    async def __write_event(self, conn, stream_name, stream_type, data):
        await conn.publish_event(stream_name, stream_type, body=data)

    async def __run_writer(self, stream_name, stream_type, data):
        async with photonpump.connect(host=self.config['host'], port=self.config['port'],
                                      username=self.config['username'], password=self.config['password']) as conn:
            await self.__write_event(conn, stream_name, stream_type, data)

    async def __read_an_event(self, conn, stream_name):
        event_data = []
        for event_record in await conn.get(stream_name):
            # print(event_record.event.type, str(event_record.event.event_number), event_record.event.json())
            eventDictionary = {"event_number": event_record.event.event_number, 'event_type': event_record.event.type}
            eventDictionary.update(event_record.event.json())
            event_data.append(eventDictionary)
        return event_data

    async def __run_reader(self, stream_name):
        async with photonpump.connect(host=self.config['host'], port=self.config['port'],
                                      username=self.config['username'], password=self.config['password']) as conn:
            return await self.__read_an_event(conn, stream_name)

    async def __event_loop(self):
        return asyncio.get_event_loop()

    def Save(self, aggregate: AggregateBase):
        event_loop = asyncio.new_event_loop()
        for event in aggregate.uncommitted_events:
            stream_type = type(event).__name__
            asyncio.set_event_loop(event_loop)
            data = json.dumps(event.__dict__)
            event_loop.run_until_complete(
                self.__run_writer(type(aggregate).__name__ + '-' + event.Id, stream_type, data))

    def event_read(self, aggregate, id):
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        json_data = {}
        try:
            json_data = event_loop.run_until_complete(self.__run_reader(type(aggregate).__name__ + '-' + id))
        except Exception:
            pass
        return json_data


if __name__ == '__main__':
    from Reservations.Domain.Aggregates.Reservation import Reservation
    from Reservations.Domain.Models.Events import ReservationMade
    from Reservations.Domain.Models.Commands import MakeReservation
    es_client = EventStoreClient()
    roomReservedCommand = MakeReservation({'Id': str(uuid.uuid4()), 'HotelId': str(uuid.uuid4()), 'RoomType': 'Presidential'})
    roomReservedEvent = ReservationMade(Id=roomReservedCommand.Id, HotelId=roomReservedCommand.HotelId, RoomType=roomReservedCommand.RoomType)
    print('room reserved event', roomReservedEvent)
    reservation=Reservation()
    reservation.uncommitted_events.append(roomReservedEvent)
    es_client.Save(reservation)
    eventList = es_client.event_read(Reservation(), roomReservedEvent.Id)
    for hydration_data in eventList:
        print(hydration_data)
