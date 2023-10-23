import { DragEvent, useState } from "react";
import { useFileUploadProps } from "../types/FileUploadTypes";
import { useFileUploadStore } from "../../store/FileUploadStore";

export default function useFileUpload(props: useFileUploadProps): Array<any> {
  const { inputFileRef, acceptedFileExtension } = props;
  const [isOver, setIsOver] = useState(false);
  const setFile = useFileUploadStore((state) => state.setFile);
  const [isFileUploadError, setError] = useState(false);

  const validateExtension = (file: File) => {
    const extension = file.name.split(".").pop();
    return extension?.toLocaleLowerCase() === acceptedFileExtension;
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const onButtonClick = () => {
    inputFileRef?.current?.click();
  };

  const handleDragOver = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsOver(true);
  };

  const handleDragLeave = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsOver(false);
  };

  const handleDrop = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();

    setIsOver(false);
    const droppedFiles = Array.from(event.dataTransfer.files);

    if (validateExtension(droppedFiles[0])) {
      setFile(droppedFiles[0]);
      setError(false);
    } else {
      setError(true);
    }
  };

  return [
    handleFileChange,
    onButtonClick,
    handleDragOver,
    handleDragLeave,
    handleDrop,
    isOver,
    isFileUploadError,
  ];
}
