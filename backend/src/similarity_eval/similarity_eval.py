from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.api_parsers.models import Author


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
        cosine = _scale_results(cosine)
        return dict(zip(abstracts, cosine))


def _scale_results(cosine: list) -> list:
    min_cos = min(cosine)
    max_cos = max(cosine)
    cosine = [(val - min_cos) / (max_cos - min_cos) for val in cosine]
    return cosine
