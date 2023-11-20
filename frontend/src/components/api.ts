import axios from "axios";

export const logout = async () => {
  const response = await axios.post("/logout");

  return response.data;
};
