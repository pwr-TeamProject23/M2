import requests
import pytest
import re
import json
from src.api_parsers.scopus_parser import ScopusParser


def test_scopus_parser_get_authors(requests_mock, scopus_pub_response):
    scopus_pub_url = re.compile("https://api.elsevier.com/content/search/")
    requests_mock.get(scopus_pub_url, json=scopus_pub_response)
    scopus_parser = ScopusParser("mock", "mock")
    authors = scopus_parser.get_authors()
    assert 'José Pereira' == authors[0].first_name


def test_scopus_parser_get_authors_100(requests_mock, scopus_pub_response):
    scopus_pub_url = re.compile("https://api.elsevier.com/content/search/")
    requests_mock.get(scopus_pub_url, json=scopus_pub_response)
    scopus_parser = ScopusParser("mock", "mock", max_authors=100)
    authors = scopus_parser.get_authors()
    assert 100 == len(authors)


def test_scopus_parser_get_authors_10(requests_mock, scopus_pub_response):
    scopus_pub_url = re.compile("https://api.elsevier.com/content/search/")
    requests_mock.get(scopus_pub_url, json=scopus_pub_response)
    scopus_parser = ScopusParser("mock", "mock", max_authors=10)
    authors = scopus_parser.get_authors()
    assert 10 == len(authors)