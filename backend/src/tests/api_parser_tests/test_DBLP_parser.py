import requests
import pytest
import re
import json
from src.api_parsers.dblp_parser import DBLPParser


def test_DBLP_parser_get_authors(requests_mock, DBLP_pub_response):
    dblp_pub_url = re.compile("https://dblp.org/search/publ/api")
    requests_mock.get(dblp_pub_url, json=DBLP_pub_response)
    dblp_parser = DBLPParser("code smells")
    authors = dblp_parser.get_authors()
    assert 'Christian' == authors[0].first_name


def test_DBLP_parser_get_authors_100(requests_mock, DBLP_pub_response):
    dblp_pub_url = re.compile("https://dblp.org/search/publ/api")
    requests_mock.get(dblp_pub_url, json=DBLP_pub_response)
    dblp_parser = DBLPParser("code smells", max_authors=100)
    authors = dblp_parser.get_authors()
    assert 100 == len(authors)

def test_DBLP_parser_get_authors_10(requests_mock, DBLP_pub_response):
    dblp_pub_url = re.compile("https://dblp.org/search/publ/api")
    requests_mock.get(dblp_pub_url, json=DBLP_pub_response)
    dblp_parser = DBLPParser("code smells", max_authors=10)
    authors = dblp_parser.get_authors()
    assert 10 == len(authors)


def test_DBLP_parser_get_affilation(requests_mock, DBLP_affiliation_response, DBLP_pub_response):
    dblp_author_url = re.compile("https://dblp.org/search/author/")
    requests_mock.get(dblp_author_url, json=DBLP_affiliation_response)
    dblp_pub_url = re.compile("https://dblp.org/search/publ/api")
    requests_mock.get(dblp_pub_url, json=DBLP_pub_response)
    dblp_parser = DBLPParser("mock", max_authors=10)
    authors = dblp_parser.get_author_affiliation("mock", "2299084")
    assert 10 == len(authors)


def test_dblp_parser_doi(requests_mock, DBLP_pub_response):
    dblp_pub_url = re.compile("https://dblp.org/search/publ/api")
    requests_mock.get(dblp_pub_url, json=DBLP_pub_response)
    scopus_parser = DBLPParser("mock", max_authors=100)
    assert "10.1145/2491956.2462171" == scopus_parser.get_authors()[4].publication.doi


def test_dblp_parser_title(requests_mock, DBLP_pub_response):
    dblp_pub_url = re.compile("https://dblp.org/search/publ/api")
    requests_mock.get(dblp_pub_url, json=DBLP_pub_response)
    scopus_parser = DBLPParser("mock", max_authors=100)
    assert "Analysis of thermal geometries on slowly rotating black holes in 4D Gauss-Bonnet gravity."\
           == scopus_parser.get_authors()[12].publication.title


def test_dblp_parser_venue(requests_mock, DBLP_pub_response):
    dblp_pub_url = re.compile("https://dblp.org/search/publ/api")
    requests_mock.get(dblp_pub_url, json=DBLP_pub_response)
    scopus_parser = DBLPParser("mock", max_authors=100)
    assert "Axioms" == scopus_parser.get_authors()[13].publication.venue
