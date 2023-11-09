import ReviewersSuggestions from "./components/ReviewersSuggestions";
import PageContainer from "../components/PageContainer";

export default function ArticleSummaryPage() {
  return (
    <PageContainer>
      <div className="h-full">
        <ReviewersSuggestions />
      </div>
    </PageContainer>
  );
}
