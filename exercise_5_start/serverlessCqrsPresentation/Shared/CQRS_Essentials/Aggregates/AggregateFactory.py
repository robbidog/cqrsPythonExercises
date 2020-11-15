from Shared.CQRS_Essentials.Aggregates.AggregateBase import AggregateBase
from importlib import import_module

from Shared.CQRS_Essentials.EventStore.EventStoreClient import EventStoreClient as event_store_client


class AggregateFactory():
    def __init__(self):
        self.es_client = event_store_client()

    def get(self, aggregate_type, aggregate_id):
        module = import_module(aggregate_type.__module__)
        class_ = getattr(module, aggregate_type.__name__)
        aggregate = class_()
        if not isinstance(aggregate, AggregateBase):
            raise Exception('Improper type used as aggregate.  Must inherit from AggregateBase')
        data_dictionary = self.es_client.event_read(aggregate, aggregate_id)
        for event_dictionary in data_dictionary:
            getattr(aggregate, 'apply')(event_dictionary)

        return aggregate
