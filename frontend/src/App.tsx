import AuthorsListing from "./components/AuthorsListing";
import FileUpload from "./components/FileUpload";
import Title from "./components/Title";

function App() {
  return (
    <div className="bg-background w-screen overflow-hidden">
      <div className="flex h-8 w-full bg-light-grey" />
      <div className="flex w-full p-8">
        <Title />
        <FileUpload />
      </div>
      <div className="w-full">
        <AuthorsListing />
      </div>
    </div>
  );
}

export default App;
