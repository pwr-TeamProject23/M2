import axios from "axios";
import { Author } from "./models";

export const getSuggestions = async (user_id: number): Promise<Author[]> => {
  const response = await axios.get(`/upload/results/${user_id}`);
  return response.data;
};
