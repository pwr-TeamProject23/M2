import { ErrorIcon } from "../../components/Icons";
import { useFileUploadStore } from "../../store/FileUploadStore";

export default function UploadError() {
  const errorMessage = useFileUploadStore((state) => state.errorMessage);

  if (errorMessage === null) {
    return null;
  }
  return (
    <div className="text-stone-900 text-xs p-1 w-fit flex space-x-2">
      <ErrorIcon />
      <div>{errorMessage}</div>
    </div>
  );
}
