import axios from "axios";
import { Search } from "./models";

export const getHistory = async (user_id: number) => {
  const response = await axios.get(`/search/history/${user_id}`);
  console.log(response.data);
  return response.data as Search[];
};
