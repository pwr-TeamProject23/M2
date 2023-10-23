import re
import os
from pdfminer.high_level import extract_text


def format_text(text, leave_paragraphs=True):
    text = re.sub("^.{1,2}$", "", text, flags=re.MULTILINE)
    if leave_paragraphs:
        text = re.sub("^\n$", "", text, flags=re.MULTILINE)
        return text
    text = re.sub("\n$", "", text, flags=re.MULTILINE)
    return text


class ArticleParser:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.text = extract_text(self.pdf_path, maxpages=2)

    def get_abstract(self) -> str:
        abstract = re.findall("(?i)abstract((?:.|\n)(?:.+\n)+)", self.text)
        if len(abstract) > 0:
            return format_text(abstract[0], False)
        raise ValueError("couldn't find the abstract")

    def get_keywords(self) -> list[str]:
        keywords = re.findall("(?i)keywords:((?:.|\n)(?:.+\n)+)", self.text)
        if len(keywords) > 0:
            keywords[0] = keywords[0].strip()
            keywords = keywords[0].split(", ")
            return keywords
        raise ValueError("couldn't find the keywords")

    def get_emails(self) -> list[str]:
        emails = re.findall("[a-zA-Z]\S+@\S+[a-zA-Z]", self.text)
        if len(emails) > 0:
            return emails
        return ""

    # from file name?
    def get_title_filename(self) -> str:
        title = os.path.basename(self.pdf_path).split("_")
        title = title[1].split(".")
        return title[0]

    def get_authors(self) -> str:
        authors = re.findall(
            "(?i)complete list of authors:((?:.|\n)*)keywords", self.text
        )
        if len(authors) > 0:
            return format_text(authors[0], False)
        return ""
