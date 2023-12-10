import axios from "axios";

export const setupAxios = () => {
  axios.defaults.baseURL = window.location.origin + "/api";
  axios.defaults.withCredentials = true;
};

export function getCookie(name: string): string | null {
  const pattern = RegExp(name + "=.[^;]*");
  const matched = document.cookie.match(pattern);
  if (matched) {
    const cookie = matched[0].split("=");
    return cookie[1];
  }
  return null;
}
