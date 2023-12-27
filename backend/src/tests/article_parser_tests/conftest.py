import json
import os

import pytest
from cryptography.fernet import Fernet

from src.articles_service import articles_parser

DIRNAME = os.path.dirname(__file__)
ARTICLES_PATH = os.path.join(DIRNAME, "articles")
ARTICLES_DATA_PATH = os.path.join(DIRNAME, "articles_data")


def decrypt(filename, k):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    f = Fernet(k)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)
    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)


def encrypt_file(filename, k):
    f = Fernet(k)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)


def pytest_configure(config):
    key = os.environ.get("ARTICLE_KEY", "pFaTEQ2vHp6lh6CZFBs2TMMK4nOrCO8a4WoIj-2Gj4M=")
    for file in os.listdir(ARTICLES_PATH):
        decrypt(ARTICLES_PATH + "/" + file, key)
    for file in os.listdir(ARTICLES_DATA_PATH):
        decrypt(ARTICLES_DATA_PATH + "/" + file, key)


@pytest.fixture(params=os.listdir(ARTICLES_PATH))
def article(request, articles_data):
    for elem in articles_data:
        if elem["name"] == request.param:
            return {
                "pdf": articles_parser.ArticleParser(
                    ARTICLES_PATH + "/" + request.param
                ),
                "data": elem,
            }
    return None


@pytest.fixture()
def articles_data():
    with open(ARTICLES_DATA_PATH + "/Article_test_data.json") as f:
        data = json.load(f)
    return data


def pytest_unconfigure(config):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    key = os.environ["ARTICLE_KEY"]
    for file in os.listdir(ARTICLES_PATH):
        encrypt_file(ARTICLES_PATH + "/" + file, key)
    for file in os.listdir(ARTICLES_DATA_PATH):
        encrypt_file(ARTICLES_DATA_PATH + "/" + file, key)
