from scholarly import scholarly
from src.api_parsers.models import Source, Publication, Author
from src.api_parsers.exceptions import MaxAuthorsReachedException
from src.similarity_eval.similarity_eval import SimilarityEvaluator


class ScholarParser:
    def __init__(
        self, keywords: str, abstract: str, min_year: int = 2010, max_authors: int = 100
    ):
        self.keywords = keywords
        self.abstract = abstract
        self.authors = []
        self.min_year = min_year
        self.max_authors = max_authors

    def get_authors(self):
        pub_generator = self._get_pubs()
        for pub in pub_generator:
            try:
                self._parse_pub_dict(pub)
            except MaxAuthorsReachedException:
                break
        sim_eval = SimilarityEvaluator(self.abstract)
        self.authors = sim_eval.update_author_similarities(self.authors)
        return self.authors

    def _get_pubs(self):
        pubs = scholarly.search_pubs(query=self.keywords, year_low=self.min_year)
        return pubs

    def _parse_pub_dict(self, pub):
        author_ids = pub["author_id"]
        if set(author_ids) == {""}:
            return
        info = pub["bib"]
        pub_data = {
            "doi": None,
            "title": info["title"],
            "year": info["pub_year"],
            "venues": [info["venue"]],
            "abstract": info["abstract"],
            "citation_count": pub["num_citations"],
            "similarity_score": 0,
        }
        publication = Publication(**pub_data)
        for author_id in author_ids:
            if author_id == "":
                continue
            author_dict = _get_auth(author_id)
            author = _parse_author_dict(author_dict, publication)
            self.authors.append(author)
            if len(self.authors) >= self.max_authors:
                raise MaxAuthorsReachedException()


def _get_auth(author_id) -> dict:
    author = scholarly.search_author_id(author_id)
    return author


def _parse_author_dict(author_dict, publication: Publication) -> Author:
    author_name = author_dict["name"]
    split_name = author_name.split()
    first_name, last_name = split_name[0], " ".join(split_name[1:])
    author_data = {
        "author_external_id": author_dict["scholar_id"],
        "first_name": first_name,
        "last_name": last_name,
        "affiliation": author_dict["affiliation"],
        "email": None,
        "source": Source.GoogleScholar,
        "publication": publication,
    }
    return Author(**author_data)
