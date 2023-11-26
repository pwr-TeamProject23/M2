import axios from "axios";
import { SuggestionsReponseModel } from "./models";

export const getSuggestions = async (
  upload_id: string,
): Promise<SuggestionsReponseModel> => {
  const response = await axios.get(`/upload/results/${upload_id}`);
  return response.data;
};
