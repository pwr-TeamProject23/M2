from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.api_parsers import ParsedAuthor


class SimilarityEvaluator:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_df=0.8, ngram_range=(1, 2))

    def update_author_similarities(
        self, input_abstract: str, authors: list[ParsedAuthor]
    ) -> list[ParsedAuthor]:
        abstracts = {
            author.publication.abstract
            for author in authors
            if author.publication.abstract
        }
        if not abstracts:
            return authors

        similarities = self._evaluate_similarities(input_abstract, list(abstracts))
        for author in authors:
            abstract = author.publication.abstract
            if abstract:
                author.publication.similarity_score = similarities.get(abstract, 0)
        return authors

    def _evaluate_similarities(
        self, input_abstract: str, abstracts: list[str]
    ) -> dict[str, float]:
        tfidf_matrix = self.vectorizer.fit_transform([input_abstract] + abstracts)
        cosine_scores = cosine_similarity(tfidf_matrix, tfidf_matrix)[0][1:]
        return dict(zip(abstracts, cosine_scores))


def _scale_values(values: list[float]) -> list[float]:
    if not values or len(set(values)) == 1:
        return values
    min_val, max_val = min(values), max(values)
    return [(val - min_val) / (max_val - min_val) for val in values]


def scale_scores(authors: list[ParsedAuthor]) -> list[ParsedAuthor]:
    similarity_scores = [author.publication.similarity_score for author in authors]
    years = [author.publication.year for author in authors]
    citations = [author.publication.citation_count for author in authors]

    scaled_scores = {
        "similarity": _scale_values(similarity_scores),
        "years": _scale_values(years),
        "citations": _scale_values(citations),
    }

    for i, author in enumerate(authors):
        combined_score = sum(scaled_scores[key][i] for key in scaled_scores) / len(
            scaled_scores
        )
        author.publication.similarity_score = combined_score

    authors.sort(key=lambda author: author.publication.similarity_score, reverse=True)
    return authors
