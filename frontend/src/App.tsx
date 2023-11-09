import HomePage from "./fileUpload/FileUploadPage";
import LoginPage from "./auth/LoginPage";
import ArticleSummaryPage from "./articleSummary/ArticleSummaryPage";
import { Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";

function App() {
  return (
    <Routes>
      <Route element={<Navbar />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/article/:articleId" element={<ArticleSummaryPage />} />
      </Route>

      <Route path="/login" element={<LoginPage />} />
      <Route path="*" element={<>404 not found</>} />
    </Routes>
  );
}

export default App;
