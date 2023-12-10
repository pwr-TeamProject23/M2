import { DragEvent, useState } from "react";
import { useFileUploadProps } from "../types/FileUploadTypes";
import { useFileUploadStore } from "../../store/FileUploadStore";
import { uploadArticle } from "./api";
import { useAuthStore } from "../../store/AuthStore";
import { useHistoryStore } from "../HistoryStore";
import { getHistory } from "../components/api";

export default function useFileUpload(props: useFileUploadProps): Array<any> {
  const { inputFileRef, acceptedFileExtension } = props;
  const [isOver, setIsOver] = useState(false);
  const { file, setFile } = useFileUploadStore((state) => ({
    file: state.file,
    setFile: state.setFile,
  }));
  const setErrorName = useFileUploadStore((state) => state.setErrorMessage);
  const user = useAuthStore((state) => state.user);
  const setSearches = useHistoryStore((state) => state.setSearches);

  const validateExtension = (file: File) => {
    const extension = file.name.split(".").pop();
    return extension?.toLocaleLowerCase() === acceptedFileExtension;
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const file = e.target.files[0];
      setFile(file);
      if (file != undefined && user != null) {
        uploadArticle(file)
          .then(setErrorName)
          .then(() => getHistory())
          .then(setSearches);
      }
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
    const file = droppedFiles[0];
    if (validateExtension(file)) {
      setFile(file);
      if (file != undefined && user != null) {
        uploadArticle(file)
          .then(setErrorName)
          .then(() => getHistory())
          .then(setSearches);
      }
    } else {
      setErrorName("File should be in PDF format");
    }
  };

  return [
    handleFileChange,
    onButtonClick,
    handleDragOver,
    handleDragLeave,
    handleDrop,
    isOver,
  ];
}
