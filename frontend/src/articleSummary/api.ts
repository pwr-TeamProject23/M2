import axios from "axios";
import { Author } from "./models";

export const getSuggestions = async (upload_id: string): Promise<Author[]> => {
  const response = await axios.get(`/upload/results/${upload_id}`);
  return response.data;
};
