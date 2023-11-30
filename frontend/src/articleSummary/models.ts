export interface Author {
  id: number;
  name: string;
  affiliation: string;
  src: string;
  year: string;
  venue: string | null;
}

export type SuggestionsResponseModel = {
  authors: Author[];
  venues: string[];
};

export type DetailsResponseModel = {
  affiliation: string;
};
