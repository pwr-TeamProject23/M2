import json
import os

import pytest
from cryptography.fernet import Fernet
from src.articles_service import articles_parser


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


def pytest_sessionstart(session):
    key = os.environ["ARTICLE_KEY"]
    for file in os.listdir("articles"):
        decrypt("articles/" + file, key)
    for file in os.listdir("articles_data"):
        decrypt("articles_data/" + file, key)


@pytest.fixture(params=os.listdir("articles"))
def article(request, articles_data):
    for elem in articles_data:
        if elem["name"] == request.param:
            return {
                "pdf": articles_parser.ArticleParser("articles/" + request.param),
                "data": elem,
            }
    return None


@pytest.fixture()
def articles_data():
    with open("articles_data/Article_test_data.json") as f:
        data = json.load(f)
    return data


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    key = os.environ["ARTICLE_KEY"]
    for file in os.listdir("articles"):
        encrypt_file("articles/" + file, key)
    for file in os.listdir("articles_data"):
        encrypt_file("articles_data/" + file, key)
