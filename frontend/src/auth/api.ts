import axios from "axios";
import { LoginCredentials, User } from "./models";

export const login = async (data: LoginCredentials) => {
  const response = await axios.post("/login", data);

  return response.data;
};

export const getLoggedUser = async () => {
  const response = await axios.get("/who_am_i");

  return response.data as User;
};
