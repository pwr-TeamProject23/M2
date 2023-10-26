import HomePage from "./fileUpload/FileUploadPage";
import LoginPage from "./auth/LoginPage";
import {Route, Routes} from 'react-router-dom';


function App() {
  return (
    <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="*" element={<>404 not found</>} />
    </Routes>
  )
}

export default App;
