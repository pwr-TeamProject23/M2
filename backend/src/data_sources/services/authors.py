from backend.src.data_sources.handlers.abstract import AbstractHandler


class AuthorsService:
    def __init__(self, *handlers: list[AbstractHandler]) -> None:
        self.handlers = handlers

    def get_authors(self):
        authors = []

        for handler in self.handlers:
            authors.extend(handler.get_authors())

        return authors
