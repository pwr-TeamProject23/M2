import os
import re
from keybert import KeyBERT

from pdfminer.high_level import extract_text


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
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.text_authors = extract_text(self.pdf_path, maxpages=1)
        self.text_main = extract_text(self.pdf_path, page_numbers={1})
        self.text_long = extract_text(self.pdf_path)

    def get_abstract(self) -> str:
        abstract = re.findall("(?i)abstract:?\n?((?:.|\n)(?:.+\n)+)", self.text_main)
        if len(abstract) == 0:
            abstract = re.findall("(?i)background:?\n?((?:.|\n)(?:.+\n)+)", self.text_main)
        if len(abstract) == 0:
            abstract = re.findall("(?i)abstract:?\n?((?:.|\n)(?:.+\n)+)", self.text_authors)
        if len(abstract) == 0:
            abstract = re.findall("(?i)abstract\n*((?:.|\n)(?:.+\n)+)", self.text_main)
        if len(abstract) > 0:
            return format_text(abstract[0], False)
        raise AbstractParsingError()

    def get_keywords(self) -> list[str]:
        keywords = re.findall("(?i)keywords:\n?((?:.|\n)(?:.+\n)+)", self.text_main)
        if len(keywords) == 0:
            keywords = re.findall("(?i)keywords--\n?((?:.|\n)(?:.+\n)+)", self.text_main)
        if len(keywords) > 0:
            for i in range(len(keywords)):
                keywords[i] = format_text(keywords[i], False)
                keywords[i] = keywords[i].split(", ")
                for a in range(len(keywords[i])):
                    keywords[i][a] = keywords[i][a].strip()
                keywords = keywords[0]
        keybert_keywords = self.get_keywords_keybert()
        if len(keybert_keywords) > 0:
            keywords.append(keybert_keywords[0])
        if len(keywords) > 0:
            return keywords
        raise KeywordParsingError()

    def get_keywords_keybert(self) -> list[str]:
        kw_model = KeyBERT()
        keywords = kw_model.extract_keywords(self.text_long, keyphrase_ngram_range=(1, 3), use_mmr=True, diversity=0.7)
        return [k[0] for k in keywords]

    def get_emails(self) -> list[str]:
        emails = re.findall("[a-zA-Z]\S+@\S+[a-zA-Z]", self.text_main)
        if len(emails) > 0:
            return emails
        return []

    def get_title_filename(self) -> str:
        title = os.path.basename(self.pdf_path).split("_")
        title = title[1].split(".")
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
