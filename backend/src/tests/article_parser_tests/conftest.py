import json
import os
from pathlib import Path
import pytest
from cryptography.fernet import Fernet
from src.articles_service import articles_parser
import tests

base_path = Path(tests.tests_path_helper.__file__).parent
articles_path = str((base_path / "article_parser_tests/articles/").resolve())
article_data_path = str((base_path / "article_parser_tests/articles_data/").resolve())


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
    key = os.environ["ARTICLE_KEY"]
    for file in os.listdir(articles_path):
        decrypt(articles_path + "/" + file, key)
    for file in os.listdir(article_data_path):
        decrypt(article_data_path + "/" + file, key)


@pytest.fixture(params=os.listdir(articles_path))
def article(request, articles_data):
    for elem in articles_data:
        if elem["name"] == request.param:
            return {
                "pdf": articles_parser.ArticleParser(articles_path + "/" + request.param),
                "data": elem,
            }
    return None


@pytest.fixture()
def articles_data():
    with open(article_data_path + "/Article_test_data.json") as f:
        data = json.load(f)
    return data


def pytest_unconfigure(config):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    key = os.environ["ARTICLE_KEY"]
    for file in os.listdir(articles_path):
        encrypt_file(articles_path + "/" + file, key)
    for file in os.listdir(article_data_path):
        encrypt_file(article_data_path + "/" + file, key)
