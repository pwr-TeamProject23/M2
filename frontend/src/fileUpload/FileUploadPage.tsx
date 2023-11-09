import FileUpload from "./components/FileUpload";
import Title from "./components/Title";
import PageContainer from "../components/PageContainer";
import History from "./components/History";

export default function HomePage() {
  return (
    <PageContainer>
      <div className="flex-1">
        <div className="flex w-full pb-8">
          <Title />
          <FileUpload />
        </div>
        <div className="w-full">
          <History />
        </div>
      </div>
    </PageContainer>
  );
}
