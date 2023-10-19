import re
from pdfminer.high_level import extract_text


def format_text(text, leave_paragraphs=True):
    text = re.sub("^.{1,2}$", "", text, flags=re.MULTILINE)
    if leave_paragraphs:
        text = re.sub("^\n$", "", text, flags=re.MULTILINE)
        return text
    text = re.sub("\n$", "", text, flags=re.MULTILINE)
    return text


class PDFparser:

    def __init__(self, pdf_name):
        self.filename = pdf_name

    def get_text(self):
        text = extract_text(self.filename)
        return format_text(text)

    def get_text_raw(self):
        return extract_text(self.filename, maxpages=1)

    # gets the article abstract
    def get_abstract(self):
        text = extract_text(self.filename, maxpages=2)
        abstract = re.findall("(?i)abstract(?:.|\n)(?:.+\n)+", text)
        if len(abstract) > 0:
            return format_text(abstract[0], False)
        return ""

    # gets the article keywords
    def get_keywords(self):
        text = extract_text(self.filename, maxpages=2)
        keywords = re.findall("(?i)keywords:((?:.|\n)(?:.+\n)+)", text)
        if len(keywords) > 0:
            keywords[0] = keywords[0].strip()
            keywords = keywords[0].split(", ")
            return keywords
        return ""

    def get_emails(self):
        text = self.get_text()
        emails = re.findall('[a-zA-Z]\S+@\S+[a-zA-Z]', text)
        if len(emails) > 0:
            return emails
        return ""

    # from file name?
    def get_title_filename(self):
        title = self.filename.split('_')
        title = title[1].split(".")
        return title[0]

    def get_authors(self):
        authors = extract_text(self.filename, maxpages=1)
        authors = re.findall("(?i)complete list of authors:(?:.|\n)*keywords", authors)
        if len(authors) > 0:
            return format_text(authors[0], False)
        return ""
