from abc import ABC, abstractmethod


class AuthorsHandler(ABC):
    @abstractmethod
    def get_authors(self):
        raise NotImplemented
