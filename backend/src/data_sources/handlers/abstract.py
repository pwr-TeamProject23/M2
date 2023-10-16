from abc import ABC, abstractmethod


class AbstractHandler(ABC):
    @abstractmethod
    def get_authors(self):
        raise NotImplemented
