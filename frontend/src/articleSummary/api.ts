import axios from "axios";
import { Author } from "./models";

export const getSuggestions = async (): Promise<Author[]> => {
  const response = await axios.get("/upload/results/");
  return response.data;
};
