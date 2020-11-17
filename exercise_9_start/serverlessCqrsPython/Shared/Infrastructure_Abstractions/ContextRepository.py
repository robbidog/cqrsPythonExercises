from __future__ import annotations
from abc import ABC, abstractmethod


class ContextRepository(ABC):
    @abstractmethod
    def Read(self,  read_model, query_model, primary_key_name):
        pass

    @abstractmethod
    def Save(self, read_model, key_name):
        pass
