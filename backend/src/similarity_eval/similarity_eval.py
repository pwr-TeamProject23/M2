from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.api_parsers.models import Author, Publication


class SimilarityEvaluator:
    def __init__(self, input_abstract: str):
        self.input_abstract = input_abstract

    def update_author_similarities(self, authors: list[Author]) -> list[Author]:
        abstracts = list(set(a.publication.abstract for a in authors))
        similarities = self.evaluate_similarities(abstracts)
        for author in authors:
            score = similarities[author.publication.abstract]
            author.publication.similarity_score = score
        return authors

    def evaluate_similarities(self, abstracts: list[str]) -> dict[str, float]:
        abstracts_unique = list(set(abstracts))
        vector = TfidfVectorizer(max_df=0.8, ngram_range=(1, 2))
        tfidf = vector.fit_transform([self.input_abstract] + abstracts_unique)
        cosine = list(cosine_similarity(tfidf, tfidf)[0][1:])
        return dict(zip(abstracts, cosine))


def _scale_results(vals: list) -> list:
    min_val = min(vals)
    max_val = max(vals)
    if max_val == min_val:
        return vals
    values = [(val - min_val) / (max_val - min_val) for val in vals]
    return values


def scale_scores(results: list[(Author, Publication)]) -> list:
    similarities = _replace_none([res[1].similarity_score for res in results])
    similarities_scaled = _scale_results(similarities)
    years_scaled = _scale_results([res[1].year for res in results])
    citations = _replace_none([res[1].citation_count for res in results])
    citations_scaled = _scale_results(citations)
    scores = [(2*s + y + c)/4 for (s, y, c) in zip(similarities_scaled, years_scaled, citations_scaled)]
    for i in range(len(results)):
        results[i][1].similarity_score = scores[i]
    results.sort(key=lambda res: res[1].similarity_score, reverse=True)
    return results


def _replace_none(vals: list[int | None]) -> list[int]:
    vals_clean = [0 if v is None else v for v in vals]
    return vals_clean
