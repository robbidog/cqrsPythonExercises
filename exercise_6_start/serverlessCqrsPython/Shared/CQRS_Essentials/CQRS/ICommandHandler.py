from __future__ import annotations
from abc import ABC, abstractmethod


class ICommandHandler(ABC):
    @abstractmethod
    def Send(self, message: list):
        pass