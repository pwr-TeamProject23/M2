from requests.exceptions import HTTPError
from src.api_handlers.dblp.handler import DblpHandler
from src.api_parsers.models import Source, Publication, Author


class DBLPParser:
    def __init__(self, keywords: str):
        self.keywords = keywords
        self.handler = DblpHandler()

    def get_authors(self):
        try:
            pub_response = self.handler.get_publications(self.keywords)
            authors: list[Author] = []
            for page in pub_response:
                page_authors = self._parse_publications_page(page)
                authors.extend(page_authors)
            return authors
        except HTTPError:
            return []

    def _parse_publications_page(self, page: dict):
        authors: list[Author] = []
        hits = page['result']['hits']['hit']
        for hit in hits:
            authors.extend(self._parse_hit_dict(hit))
        return authors

    def _parse_hit_dict(self, hit: dict):
        authors: list[Author] = []
        info = hit['info']
        pub_data = {
            'title': info['title'],
            'abstract': '',
            'citations': 0,
            'year': info['year'],
            'source_api': Source.DBLP,
        }
        publication = Publication(**pub_data)
        authors_list = info['authors']['author']
        for author in authors_list:
            author_id = author['@pid']
            author_name = author['text']
            auth_data = {
                'name': author_name,
                'api_id': author_id,
                'publication': publication,
            }
            affiliation = self._get_author_affiliation(author_name=author_name, author_id=author_id)
            if affiliation == '':
                continue
            auth_data['affiliation'] = affiliation
            authors.append(Author(**auth_data))
        return authors

    def _get_author_affiliation(self, author_name: str, author_id: str):
        author_response = self.handler.get_authors(author_name)
        for page in author_response:
            affiliation = _extract_affiliation(author_id, page)
            if affiliation is not None:
                return affiliation
        return ''


def _extract_affiliation(author_id: str, page: dict) -> str | None:
    results = page['result']['hits']['hit']
    for hit in results:
        info = hit['info']
        if author_id not in info['url']:
            continue
        elif 'notes' not in info:
            return ''
        else:
            note = info['notes']['note']
            if type(note) != list:
                return note['text'] if note['@type'] == 'affiliation' else ''
            for n in note:
                if n['@type'] == 'affiliation':
                    return n['text']
    return None
