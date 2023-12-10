import requests
import pytest
import re
import json
from src.api_parsers.scopus_parser import ScopusParser


def test_scopus_parser_get_authors(scopus_request):
    authors = scopus_request.get_authors()
    assert 'José Pereira' == authors[0].first_name


def test_scopus_parser_get_authors_100(scopus_request):
    authors = scopus_request.get_authors()
    assert 100 == len(authors)


def test_scopus_parser_get_authors_10(requests_mock, scopus_pub_response):
    scopus_pub_url = re.compile("https://api.elsevier.com/content/search/")
    requests_mock.get(scopus_pub_url, json=scopus_pub_response)
    scopus_parser = ScopusParser("mock", "mock", max_authors=10)
    authors = scopus_parser.get_authors()
    assert 10 == len(authors)


def test_scopus_parser_citation_count_nonzero(scopus_request):
    assert 1 == scopus_request.get_authors()[32].publication.citation_count


def test_scopus_parser_citation_count_zero(scopus_request):
    assert 0 == scopus_request.get_authors()[4].publication.citation_count


def test_scopus_parser_doi(scopus_request):
    assert "10.1109/ICIRCA57980.2023.10220911" == scopus_request.get_authors()[4].publication.doi


def test_scopus_parser_title(scopus_request):
    assert "Improved Flaky Test Detection with Black-Box Approach and Test Smells"\
           == scopus_request.get_authors()[12].publication.title



