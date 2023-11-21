import axios, { AxiosError } from "axios";
import { Author } from "../../articleSummary/models";

export const uploadArticle = async (file: File, setSuggestions: (authors: Author[]) => void): Promise<string | null> => {
  let formData = new FormData();
  formData.append("file", file);
  const headers = {
    headers: {
      "Content-Type": "multipart/form-data",
      accept: "application/json",
    },
  };
  try {
    const response = await axios.post("/get_authors", formData, headers);
    setSuggestions(response.data);
  } catch (err: unknown) {
    if (err instanceof AxiosError) {
      if (err.response) {
        return err.response.data.detail;
      }
      return "Internal server error";
    }
  }

  return null;
};
