import { ErrorIcon } from "./Icons";

export default function Error(props: { isError: Boolean }) {
  if (props.isError) {
    return (
      <div className="text-red text-xs p-1 w-fit flex space-x-2">
        <ErrorIcon />
        <div>Uploaded file should be in PDF format</div>
      </div>
    );
  }
  return null;
}
