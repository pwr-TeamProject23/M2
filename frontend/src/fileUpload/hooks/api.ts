import axios, { AxiosError } from "axios";

export const uploadArticle = async (
  file: File,
  user_id: number,
): Promise<string | null> => {
  let formData = new FormData();
  formData.append("file", file);
  const headers = {
    headers: {
      "Content-Type": "multipart/form-data",
      accept: "application/json",
    },
  };
  try {
    await axios.post(`/upload/file/${user_id}`, formData, headers);
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
