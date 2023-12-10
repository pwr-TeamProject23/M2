import pytest
import requests_mock
from src.api_handlers.dblp.handler import DblpHandler
from src.api_parsers.dblp_parser import DBLPParser
from src.api_parsers.scopus_parser import ScopusParser
from pathlib import Path
import tests.tests_path_helper
import json
import re
import os


base_path = Path(tests.tests_path_helper.__file__).parent
dblp_data_path = (base_path / "api_parser_tests/api_responses/dblp.txt").resolve()
dblp_affiliation_data_path = (base_path / "api_parser_tests/api_responses/dblp_author.txt").resolve()
scopus_data_path = (base_path / "api_parser_tests/api_responses/scopus.txt").resolve()


@pytest.fixture
def DBLP_parser_mock(requests_mock):
    dblp_parser = DBLPParser()
    return


@pytest.fixture
def DBLP_pub_response():
    with open(dblp_data_path, "rb") as file:
        return json.load(file)


@pytest.fixture
def DBLP_affiliation_response():
    with open(dblp_affiliation_data_path, "rb") as file:
        return json.load(file)


@pytest.fixture
def scopus_pub_response():
    with open(scopus_data_path, "rb") as file:
        return json.load(file)


@pytest.fixture
def scopus_request(requests_mock, scopus_pub_response):
    scopus_pub_url = re.compile("https://api.elsevier.com/content/search/")
    requests_mock.get(scopus_pub_url, json=scopus_pub_response)
    return ScopusParser("mock", "mock", max_authors=100)


@pytest.fixture
def dblp_request(requests_mock, DBLP_pub_response):
    scopus_pub_url = re.compile("https://dblp.org/search/publ/api")
    requests_mock.get(scopus_pub_url, json=DBLP_pub_response)
    return DBLPParser("mock", max_authors=100)
