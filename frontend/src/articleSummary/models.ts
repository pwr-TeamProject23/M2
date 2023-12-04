export type Publication = {
  doi: string | null;
  title: string;
  year: number;
  venues: string[] | null;
  citationCount: number | null;
  similarityScore: number | null;
};

export type Author = {
  id: number;
  firstName: string;
  lastName: string;
  email: string;
  source: string;
  publication: Publication;
};

export type SuggestionsResponseModel = {
  authors: Author[];
  venues: string[];
};

export type DetailsResponseModel = {
  affiliation: string;
};
