import AuthorsListing from "./components/AuthorsListing";
import FileUpload from "./components/FileUpload";
import Title from "./components/Title";

export default function HomePage() {
  return (
    <div className="bg-background w-screen min-h-screen max-h-fit flex flex-col">
      <div className="flex h-8 w-full bg-light-grey" />
      <div className="p-8 flex-1">
        <div className="flex w-full pb-8">
          <Title />
          <FileUpload />
        </div>
        <div className="w-full bg-background">
          <AuthorsListing />
        </div>
      </div>
    </div>
  );
}
