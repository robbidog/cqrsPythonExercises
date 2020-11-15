import logging
from typing import Dict, Callable, Type, Union

from Shared.Infrastructure_Abstractions.ContextRepository import ContextRepository

from Shared.CQRS_Essentials.CQRS.Command import Command
from Shared.CQRS_Essentials.CQRS.Event import Event
from Shared.CQRS_Essentials.CQRS.IBus import IBus
from Shared.CQRS_Essentials.CQRS.Query import Query

logger = logging.getLogger(__name__)


class Bus(IBus):
    Message = Union[Command, Event, Query]

    def __init__(self,
                 command_handlers: Dict[Type[Command], Callable],
                 event_denormalizers: Dict[Type[Event], Callable],
                 query_handlers: Dict[Type[Query], Callable],
                 context_repository: ContextRepository):
        self.COMMAND_HANDLERS = command_handlers
        self.EVENT_HANDLERS = event_denormalizers
        self.QUERY_HANDLERS = query_handlers
        self.context_repository = context_repository

    def handle(self, message: Message):
        queue = [message]
        while queue:
            message = queue.pop(0)

            if isinstance(message, Command):
                self.handle_command(message)
            elif isinstance(message, Event):
                self.handle_event(message)
            elif isinstance(message, Query):
                return self.handle_query(message)
            else:
                raise Exception(f'{message} was not a Command or an event or a query')

    def handle_command(self,
                       command: Command
                       ):
        logger.info('handling command %s of type %s', command, type(command).__name__)
        handler = self.COMMAND_HANDLERS[type(command)]()
        events = handler.Send(command)
        for event in events:
            self.handle(event)

    def handle_event(self,
                     event: Event
                     ):
        logger.info('handling event %s of type %s', event, type(event).__name__)
        handler = self.EVENT_HANDLERS[type(event)](self.context_repository)
        handler.Publish(event)

    def handle_query(self,
                     query: Query
                     ):
        logger.info('handling query %s of type %s', query, type(query).__name__)
        handler = self.QUERY_HANDLERS[type(query)](self.context_repository)
        return handler.Handle(query)
