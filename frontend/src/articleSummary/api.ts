import axios from "axios";
import {
  SuggestionsResponseModel,
  DetailsResponseModel,
  FilenameResponseModel,
} from "./models";

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
): Promise<DetailsResponseModel | undefined> => {
  try {
    const response = await axios.get(
      `/search/${search_id}/source/${source}/author/${author_id}/details`,
    );
    return response.data;
  } catch {
    return undefined;
  }
};

export const getFilename = async (
  search_id: string,
): Promise<FilenameResponseModel> => {
  const response = await axios.get(`/search/${search_id}/filename`);
  return response.data;
};
