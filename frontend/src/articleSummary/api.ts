import axios from "axios";
import { SuggestionsResponseModel, DetailsResponseModel } from "./models";

export const getSuggestions = async (
  search_id: string,
): Promise<SuggestionsResponseModel> => {
  const response = await axios.get(`/search/${search_id}/results`);
  return response.data;
};

export const getDetails = async (
  search_id: string,
  source: string,
  author_id: number,
): Promise<DetailsResponseModel> => {
  const response = await axios.get(
    `/search/${search_id}/source/${source}/author/${author_id}/details`,
  );
  return response.data;
};
