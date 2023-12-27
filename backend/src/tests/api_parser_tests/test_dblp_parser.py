import re

from src.api_parsers.dblp import DblpParser


def test_dblp_parser_get_authors(dblp_request):
    authors = dblp_request.get_authors()
    assert "Christian" == authors[0].first_name


def test_dblp_parser_get_authors_100(dblp_request):
    authors = dblp_request.get_authors()
    assert 100 == len(authors)


def test_dblp_parser_get_authors_10(requests_mock, dblp_pub_response):
    dblp_pub_url = re.compile("https://dblp.org/search/publ/api")
    requests_mock.get(dblp_pub_url, json=dblp_pub_response)
    dblp_parser = DblpParser()
    authors = dblp_parser.get_authors_and_publications(keywords="code smells")
    assert 10 == len(authors)


def test_dblp_parser_get_affiliation(
    requests_mock, dblp_affiliation_response, dblp_pub_response
):
    dblp_author_url = re.compile("https://dblp.org/search/author/")
    requests_mock.get(dblp_author_url, json=dblp_affiliation_response)
    dblp_pub_url = re.compile("https://dblp.org/search/publ/api")
    requests_mock.get(dblp_pub_url, json=dblp_pub_response)
    dblp_parser = DblpParser()
    authors = dblp_parser.get_author_affiliation("mock", "2299084")
    assert 10 == len(authors)


def test_dblp_parser_doi(dblp_request):
    assert "10.1145/2491956.2462171" == dblp_request.get_authors()[4].publication.doi


def test_dblp_parser_title(dblp_request):
    assert (
        "Analysis of thermal geometries on slowly rotating black holes in 4D Gauss-Bonnet gravity."
        == dblp_request.get_authors()[12].publication.title
    )


def test_dblp_parser_venue(dblp_request):
    assert "Axioms" == dblp_request.get_authors()[13].publication.venues[0]
