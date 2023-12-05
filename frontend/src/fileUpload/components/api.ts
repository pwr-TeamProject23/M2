import axios from "axios";
import { Search, SearchStatus } from "./models";

export const getHistory = async (user_id: number) => {
  const response = await axios.get(`/search/history/${user_id}`);
  console.log(user_id, response.data)
  return response.data as Search[];
};

export const getSearchStatus = async (search_id: number) => {
  const response = await axios.get(`/search/${search_id}/status`);
  return response.data.status as SearchStatus;
};
