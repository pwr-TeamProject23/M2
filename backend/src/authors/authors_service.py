from backend.src.authors.handlers.abstract_handler import AuthorsHandler


class AuthorsService:
    def __init__(self, *handlers: list[AuthorsHandler]) -> None:
        self.handlers = handlers

    def get_authors(self):
        authors = []

        for handler in self.handlers:
            authors.extend(handler.get_authors())

        return authors
