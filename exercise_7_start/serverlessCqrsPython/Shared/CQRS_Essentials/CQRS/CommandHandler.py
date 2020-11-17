from __future__ import annotations
from abc import ABC, abstractmethod


class CommandHandler(ABC):
    @abstractmethod
    def Send(self, message: list):
        pass