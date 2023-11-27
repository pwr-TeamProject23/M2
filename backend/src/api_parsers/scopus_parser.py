from src.api_parsers.exceptions import NoAuthorsException, MaxAuthorsReachedException
from src.api_handlers.scopus.handler import ScopusHandler
from src.api_parsers.models import Source, Publication, Author
from src.similarity_eval.similarity_eval import SimilarityEvaluator
from requests.exceptions import HTTPError


class ScopusParser:
    def __init__(self, keywords: str, abstract: str, min_year: int = 2010, max_authors: int = 100):
        self.keywords = keywords
        self.abstract = abstract
        self.handler = ScopusHandler()
        self.authors = []
        self.min_year = min_year
        self.max_authors = max_authors

    def _get_author_affiliation(self, author_id: str) -> str:
        params = {"view": "ENHANCED"}
        author_response = self.handler.get_author_by_id(
            author_id=author_id, params=params
        )
        affiliation = _extract_affiliation(author_response)
        return affiliation

    def get_authors(self) -> list[Author]:
        pub_params = {
            "query": f"TITLE-ABS-KEY({self.keywords})",
            "view": "COMPLETE",
        }
        try:
            pub_response = self.handler.get_abstracts_and_citations(params=pub_params)
        except HTTPError:
            raise NoAuthorsException(self.keywords)
        for page in pub_response:
            if "error" in page:
                raise NoAuthorsException(self.keywords)
            try:
                self._parse_publications_page(page)
            except MaxAuthorsReachedException:
                break
        sim_eval = SimilarityEvaluator(self.abstract)
        self.authors = sim_eval.update_author_similarities(self.authors)
        return self.authors

    def _parse_entry_dict(self, entry: dict) -> None:
        year = int(entry["prism:coverDate"].split("-")[0])
        if year < self.min_year:
            return
        pub_data = {
            "title": entry["dc:title"],
            "abstract": entry.get("dc:description"),
            "citations": entry.get("citedby-count"),
            "venue": '',
            "year": year,
            "source_api": Source.SCOPUS,
            "similarity_score": None,
        }
        publication = Publication(**pub_data)
        if "author" not in entry:
            return
        authors_list = entry["author"]
        for author in authors_list:
            first_name = author.get("given-name")
            last_name = author.get("surname")
            if first_name is None and last_name is None:
                continue
            author_id = author["authid"]
            auth_data = {
                "first_name": first_name,
                "last_name": last_name,
                "api_id": author_id,
                "publication": publication,
                "affiliation": self._get_author_affiliation(author_id=author_id),
            }
            author = Author(**auth_data)
            print(author)
            self.authors.append(author)
            if len(self.authors) >= self.max_authors:
                raise MaxAuthorsReachedException()

    def _parse_publications_page(self, page: dict) -> None:
        entries = page["search-results"]["entry"]
        for entry in entries:
            self._parse_entry_dict(entry)


def _extract_affiliation(author_response: dict) -> str:
    profile = author_response["author-retrieval-response"][0]["author-profile"]
    affiliation = profile["affiliation-current"]["affiliation"]
    if type(affiliation) == list:
        return affiliation[0]["ip-doc"]["afdispname"]
    return affiliation["ip-doc"]["afdispname"]



s = ScopusParser('code smells', "Replication of research experiments is important for establishing the validity and "
                                 "generalizability of findings, building a cumulative body of knowledge, "
                                 "and addressing issues of publication bias. The quest for replication led to the "
                                 "concept of scientific workflow, a structured and systematic process for carrying "
                                 "out research that defines a series of steps, methods, and tools needed to collect "
                                 "and analyze data, and generate results. In this study, we propose a cloud-based "
                                 "framework built upon open source software, which facilitates the construction and "
                                 "execution of workflows for the replication/reproduction of software quality "
                                 "studies. To demonstrate its feasibility, we describe the replication of a software "
                                 "quality experiment on automatically detecting code smells with machine learning "
                                 "techniques. The proposed framework can mitigate two types of validity threats in "
                                 "software quality experiments: (i) internal validity threats due to instrumentation, "
                                 "since the same measurement instruments can be used in replications, "
                                 "thus not affecting the validity of the results, and (ii) external validity threats "
                                 "due to reduced generalizability, since different researchers can more easily "
                                 "replicate experiments with different settings, populations, and contexts while "
                                 "reusing the same scientific workflow.", max_authors=10).get_authors()
for a in s:
    print(a)
print(len(s))