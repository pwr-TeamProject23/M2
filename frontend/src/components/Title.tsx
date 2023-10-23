const reviewedBanner =
  "Bleeding edge support system for discovering most suitable reviewers as simple as uploading a file. To get started upload a file in PDF format.";

export default function Title() {
  return (
    <div className="">
      <div className="text-white text-7xl">Reviewed</div>
      <div className="text-white text-s font-extralight w-2/3">
        {reviewedBanner}
      </div>
    </div>
  );
}
