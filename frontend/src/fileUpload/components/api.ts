import axios from "axios";
import { Upload } from "./models";

export const getHistory = async (user_id: number) => {
  const response = await axios.get(`/upload/history/${user_id}`);
  console.log(response.data);
  return response.data as Upload[];
};
