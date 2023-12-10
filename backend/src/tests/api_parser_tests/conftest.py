import json
import os
import re
from pathlib import Path

import pytest
import requests_mock

from src.api_handlers.dblp.handler import DblpHandler
from src.api_parsers.dblp import DblpParser
from src.api_parsers.scopus import ScopusParser

DIRNAME = os.path.dirname(__file__)
DBLP_DATA_PATH = os.path.join(DIRNAME, "api_responses/dblp.txt")
DBLP_AFFILIATION_DATA_PATH = os.path.join(DIRNAME, "api_responses/dblp_author.txt")
SCOPUS_DATA_PATH = os.path.join("api_responses/scopus.txt")


@pytest.fixture
def dblp_pub_response():
    with open(DBLP_DATA_PATH, "rb") as file:
        return json.load(file)


@pytest.fixture
def dblp_affiliation_response():
    with open(DBLP_AFFILIATION_DATA_PATH, "rb") as file:
        return json.load(file)


@pytest.fixture
def scopus_pub_response():
    with open(SCOPUS_DATA_PATH, "rb") as file:
        return json.load(file)


@pytest.fixture
def scopus_request(requests_mock, scopus_pub_response):
    scopus_pub_url = re.compile("https://api.elsevier.com/content/search/")
    requests_mock.get(scopus_pub_url, json=scopus_pub_response)
    return ScopusParser("mock", "mock", max_authors=100)


@pytest.fixture
def dblp_request(requests_mock, dblp_pub_response):
    scopus_pub_url = re.compile("https://dblp.org/search/publ/api")
    requests_mock.get(scopus_pub_url, json=dblp_pub_response)
    return DblpParser()
