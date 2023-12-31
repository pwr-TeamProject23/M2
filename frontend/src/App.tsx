import HomePage from "./fileUpload/FileUploadPage";
import LoginPage from "./auth/LoginPage";
import ArticleSummaryPage from "./articleSummary/ArticleSummaryPage";
import { Route, Routes, useNavigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import React, { useEffect } from "react";
import { useAuthStore } from "./store/AuthStore";

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
  }, []);

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
            <Navbar />
          </Protected>
        }
      >
        <Route path="/" element={<HomePage />} />
        <Route path="/search/:searchId" element={<ArticleSummaryPage />} />
      </Route>
      <Route path="/login" element={<LoginPage />} />
      <Route path="*" element={<>404 not found</>} />
    </Routes>
  );
}

export default App;
