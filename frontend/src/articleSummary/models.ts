export interface Author {
  id: number;
  name: string;
  affiliation: string;
  email: string;
  src: string;
  year: string;
  venue: string | null;
}

export type SuggestionsReponseModel = {
  authors: Author[];
  venues: string[];
};
