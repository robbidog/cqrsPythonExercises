from __future__ import annotations
from abc import ABC, abstractmethod


class AggregateBase(ABC):
    uncommitted_events = []
    State = {}
    def __init__(self):
        pass

    def dump_state(self):
        attrs = vars(self.State)
        print(', '.join("%s: %s" % item for item in attrs.items()))

    @abstractmethod
    def apply(self, data_dictionary: dict):
        pass
