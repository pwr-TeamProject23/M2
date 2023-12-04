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
  source: string;
  publication: Publication;
};

export type SuggestionsResponseModel = {
  authors: Author[];
  venues: string[];
  filename: string;
};

export type DetailsResponseModel = {
  affiliation: string;
};

export type FilenameResponseModel = {
  file_name: string;
}