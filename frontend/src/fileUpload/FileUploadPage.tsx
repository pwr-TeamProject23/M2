import FileUpload from "./components/FileUpload";
import Title from "./components/Title";
import PageContainer from "../components/PageContainer";
import ReviewersSuggestions from "../articleSummary/components/ReviewersSuggestions";

export default function HomePage() {
  return (
    <PageContainer>
      <div className="flex-1">
        <div className="flex w-full pb-8">
          <Title />
          <FileUpload />
        </div>
        <div className="w-full">
          <ReviewersSuggestions />
        </div>
      </div>
    </PageContainer>
  );
}
