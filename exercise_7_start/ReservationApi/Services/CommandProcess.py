from __future__ import annotations
import abc


# implemented properly, using the 'with' statement, all error handling could be implemented here for improper commands
class CommandProcess(abc.ABC):

    def __enter__(self) -> CommandProcess:
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    # @abc.abstractmethod
    # def _commit(self):
    #     raise NotImplementedError
    #
    # @abc.abstractmethod
    # def rollback(self):
    #     raise NotImplementedError
