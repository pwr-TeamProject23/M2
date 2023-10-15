import { useRef } from "react";
import useFileUpload from "../hooks/useDragAndDropFile";
import Error from "./Error";
import { CheckmarkIcon, UploadIcon } from "./Icons";
import { FileUploadProps } from "../types/FileUploadTypes";


function FileUploadPrompt(props: FileUploadProps) {
  const { inputFileRef, handleFileChange, onButtonClick, isOver } = props;

  return (
    <div className="gird justify-items-center">
      <div className={isOver ? "" : "animate-bounce"}>
        <UploadIcon />
      </div>

      <div className="flex space-x-1">
        <div className="font-roboto text-gray-300 text-s">Select file to</div>
        <input
          type="file"
          id="article-upload"
          ref={inputFileRef}
          className="hidden"
          onChange={handleFileChange}
          accept=".pdf"
          maxLength={1}
        />
        <button className="text-accent text-s" onClick={onButtonClick}>
          Upload
        </button>
      </div>

      <div className="text-[#676767] text-xs flex justify-center">
        Supported formats: PDF
      </div>
    </div>
  );
}

function FileUploaded(props: { filename: string }) {
  return (
    <div className="grid justify-items-center">
      <CheckmarkIcon />
      <div className="text-gray-300 text-s">Upload was successful</div>
      <div className="text-accent text-m mx-4 text-center">
        {props.filename}
      </div>
    </div>
  );
}

export default function FileUpload() {
  const inputFileRef = useRef<HTMLInputElement | null>(null);
  const [
    handleFileChange,
    onButtonClick,
    handleDragOver,
    handleDragLeave,
    handleDrop,
    isOver,
    file,
    isFileUploadError,
  ] = useFileUpload({
    inputFileRef: inputFileRef,
    acceptedFileExtension: "pdf",
  });

  return (
    <>
      <Error isError={isFileUploadError} />
      <div
        className="border border-dashed border-accent bg-light-grey rounded-md w-64 h-48 flex items-center justify-center"
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <div className="grid">
          {file === null ? (
            <FileUploadPrompt
              handleFileChange={handleFileChange}
              onButtonClick={onButtonClick}
              inputFileRef={inputFileRef}
              isOver={isOver}
            />
          ) : (
            <FileUploaded filename={file.name} />
          )}
        </div>
      </div>
    </>
  );
}
