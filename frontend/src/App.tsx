import HomePage from "./fileUpload/FileUploadPage";
import LoginPage from "./auth/LoginPage";
import ArticleSummaryPage from "./articleSummary/ArticleSummaryPage";
import { Route, Routes, useNavigate, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import React, { useEffect } from "react";
import { useAuthStore } from "./auth/store";

const Protected = (props: { children: React.ReactNode }) => {
  const { authenticate: authenticate, user } = useAuthStore();
  const navigate = useNavigate();

  useEffect(() => {
    authenticate()
      .then(() => {
        return props.children;
      })
      .catch(() => {
        navigate("/login");
      });
  }, [user]);

  if (!user) {
    return null;
  }

  return props.children;
};

function App() {
  return (
    <Routes>
      <Route
        element={
          <Protected>
            {" "}
            <Navbar />{" "}
          </Protected>
        }
      >
        <Route path="/" element={<HomePage />} />
        <Route path="/article/:articleId" element={<ArticleSummaryPage />} />
      </Route>
      <Route path="/login" element={<LoginPage />} />
      <Route path="*" element={<>404 not found</>} />
    </Routes>
  );
}

export default App;
