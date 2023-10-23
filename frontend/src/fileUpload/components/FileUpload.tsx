import { useRef } from "react";
import useFileUpload from "../hooks/useDragAndDropFile";
import Error from "./Error";
import { CheckmarkIcon, UploadIcon } from "./Icons";
import { FileUploadProps } from "../types/FileUploadTypes";
import { useFileUploadStore } from "../../store/FileUploadStore";

function FileUploadPrompt(props: FileUploadProps) {
  const { inputFileRef, handleFileChange, onButtonClick, isOver } = props;

  return (
    <div className="gird justify-items-center">
      <div className={isOver ? "" : "animate-bounce"}>
        <UploadIcon />
      </div>

      <div className="flex space-x-1 mb-4">
        <div className="font-roboto text-gray-300 text-s">
          Drag & drop files
        </div>
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
          Browse
        </button>
      </div>

      <div className="text-[#676767] text-xs flex justify-center">
        Supported formats: PDF
      </div>
    </div>
  );
}

function FileUploaded() {
  const file = useFileUploadStore((state) => state.file);
  return (
    <div className="grid justify-items-center">
      <CheckmarkIcon />
      <div className="text-gray-300 text-s">Upload was successful</div>
      <div className="text-accent text-m mx-4 text-center">
        {file?.name}
      </div>
    </div>
  );
}

export default function FileUpload() {
  const inputFileRef = useRef<HTMLInputElement | null>(null);
  const file = useFileUploadStore((state) => state.file);
  const [
    handleFileChange,
    onButtonClick,
    handleDragOver,
    handleDragLeave,
    handleDrop,
    isOver,
    isFileUploadError,
  ] = useFileUpload({
    inputFileRef: inputFileRef,
    acceptedFileExtension: "pdf",
  });

  return (
    <div className="w-1/2">
      <div
        className="border border-dashed border-accent bg-light-grey rounded-md h-48 flex items-center justify-center"
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <div className="grid">
          {file === undefined ? (
            <FileUploadPrompt
              handleFileChange={handleFileChange}
              onButtonClick={onButtonClick}
              inputFileRef={inputFileRef}
              isOver={isOver}
            />
          ) : (
            <FileUploaded />
          )}
        </div>
      </div>
      <Error isError={isFileUploadError} />
    </div>
  );
}
