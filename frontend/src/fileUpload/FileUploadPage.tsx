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
          <div className="text-stone-900 text-3xl pb-4 border-b border-stone-300">
            Your uploads
          </div>
          <History />
        </div>
      </div>
    </PageContainer>
  );
}
