import os
import re
from collections import Counter
from logging import getLogger

import spacy
from pdfminer.high_level import extract_text

logger = getLogger(__name__)


def format_text(text, leave_paragraphs=True):
    text = re.sub("^.{1,2}$", "", text, flags=re.MULTILINE)
    if leave_paragraphs:
        text = re.sub("^\n$", "", text, flags=re.MULTILINE)
        return text
    text = re.sub("\n$", "", text, flags=re.MULTILINE)
    return text.strip()


class ArticleParsingError(Exception):
    def __init__(self, message="Couldn't parse the pdf file"):
        self.message = message
        super().__init__(self.message)


class AbstractParsingError(ArticleParsingError):
    def __init__(self, message="Couldn't retrieve the abstract from the pdf file"):
        self.message = message
        super().__init__(self.message)


class KeywordParsingError(ArticleParsingError):
    def __init__(self, message="Couldn't retrieve the keywords from the pdf file"):
        self.message = message
        super().__init__(self.message)


class AuthorParsingError(ArticleParsingError):
    def __init__(self, message="Couldn't retrieve the authors list from the pdf file"):
        self.message = message
        super().__init__(self.message)


class ArticleParser:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.text_authors = extract_text(self.pdf_path, maxpages=1)
        self.text_main = extract_text(self.pdf_path, page_numbers={1})
        self.text_long = extract_text(self.pdf_path)

    def get_abstract(self) -> str:
        abstract = re.findall("(?i)abstract:?\n?((?:.|\n)(?:.+\n)+)", self.text_main)
        if len(abstract) == 0:
            abstract = re.findall(
                "(?i)background:?\n?((?:.|\n)(?:.+\n)+)", self.text_main
            )
        if len(abstract) == 0:
            abstract = re.findall(
                "(?i)abstract:?\n?((?:.|\n)(?:.+\n)+)", self.text_authors
            )
        if len(abstract) == 0:
            abstract = re.findall("(?i)abstract\n*((?:.|\n)(?:.+\n)+)", self.text_main)
        if len(abstract) > 0:
            return format_text(abstract[0], False)

    def get_keywords(self) -> list[str]:
        keywords = self.get_spacy_keywords()
        if not keywords:
            parsed_keywords = re.findall(
                "(?i)keywords:\n?((?:.|\n)(?:.+\n)+)", self.text_main
            )
            if len(keywords) == 0:
                parsed_keywords = re.findall(
                    "(?i)keywords--\n?((?:.|\n)(?:.+\n)+)", self.text_main
                )
            if len(parsed_keywords) > 0:
                for i in range(len(parsed_keywords)):
                    parsed_keywords[i] = format_text(parsed_keywords[i], False)
                    parsed_keywords[i] = parsed_keywords[i].split(", ")
                    for a in range(len(parsed_keywords[i])):
                        parsed_keywords[i][a] = parsed_keywords[i][a].strip()
                    parsed_keywords = parsed_keywords[0]

            keywords.extend(parsed_keywords)

        if len(keywords) > 0:
            return list(set(keywords))
        raise KeywordParsingError()

    def get_spacy_keywords(self, n_most_common: int = 5) -> list[str]:
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(self.text_main.lower())
        keywords = [
            token.lemma_
            for token in doc
            if token.pos_ in ("NOUN", "ADJ", "VERB")
            and not token.is_stop
            and not token.is_punct
        ]
        logger.info(f"SpaCy found keywords: {keywords}")
        most_common = Counter(keywords).most_common(n_most_common)
        return [counted[0] for counted in most_common]

    def get_emails(self) -> list[str]:
        emails = re.findall("[a-zA-Z]\S+@\S+[a-zA-Z]", self.text_main)
        if len(emails) > 0:
            return emails
        return []

    def get_title(self) -> str:
        title = re.findall(
            "(?i)e-Informatica Software Engineering Journal\n?((?:.|\n)(?:.+\n)+)\nJournal",
            self.text_authors,
        )
        return title[0]

    def get_authors(self) -> list[str]:
        authors = re.findall(
            "(?i)complete list of authors:((?:.|\n)*?)keywords", self.text_authors
        )
        if len(authors) > 0:
            authors = format_text(authors[0], False)
            authors = re.findall("^(.*?);", authors, flags=re.MULTILINE)
            for i in range(len(authors)):
                authors[i] = authors[i].strip()
            return authors
        raise AuthorParsingError()
