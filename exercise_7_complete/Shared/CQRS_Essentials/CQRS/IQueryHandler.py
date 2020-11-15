from __future__ import annotations
from abc import ABC, abstractmethod


class IQueryHandler(ABC):
    @abstractmethod
    def Handle(self, message: list):
        pass
