import pytest
from backend.src.articles_service import articles_parser
import os


# pytestmark = pytest.mark.parametrize("article", os.listdir("articles"), indirect=True)


def test_get_keywords(article):
    keywords = article.get_keywords()
    assert len(keywords) >= 1


def test_get_abstract(article):
    abstract = article.get_abstract()
    assert len(abstract) >= 100


def test_get_authors(article):
    authors = article.get_authors()
    assert len(authors) >= 1


def test_get_emails(article):
    emails = article.get_emails()
    assert len(emails) >= 1
