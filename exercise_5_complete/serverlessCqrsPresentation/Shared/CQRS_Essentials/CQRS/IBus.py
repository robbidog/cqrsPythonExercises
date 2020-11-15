from __future__ import annotations
from abc import ABC, abstractmethod


class IBus(ABC):
    @abstractmethod
    def handle(self, message: list):
        pass

    @abstractmethod
    def handle_command(self, command):
        pass

    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def handle_query(self, query:Query):
        pass
