import { ErrorIcon } from "../../components/Icons";

export default function Error(props: { isError: Boolean }) {
  if (props.isError) {
    return (
      <div className="text-white text-xs p-1 w-fit flex space-x-2">
        <ErrorIcon />
        <div>Uploaded file is required to be in PDF format</div>
      </div>
    );
  }
  return null;
}
