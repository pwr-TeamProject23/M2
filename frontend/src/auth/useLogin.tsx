import { LoginCredentials } from "./models";
import { login } from "./api";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

export default function useLogin() {
  const navigate = useNavigate();
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const onLoginSubmit = (values: LoginCredentials) => {
    login(values)
      .then(() => {
        navigate("/");
      })
      .catch(() => {
        setErrorMessage("Invalid email or password");
      });
  };

  return {
    onLoginSubmit,
    errorMessage,
  };
}
