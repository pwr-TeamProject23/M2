interface FileUpload {
  inputFileRef: React.MutableRefObject<HTMLInputElement | null>;
  acceptedFileExtension: string;
  handleFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onButtonClick: () => void;
  isOver: boolean;
}

export type useFileUploadProps = Pick<
  FileUpload,
  "inputFileRef" | "acceptedFileExtension"
>;

export type FileUploadProps = Omit<FileUpload, "acceptedFileExtension">;
