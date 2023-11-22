export enum UploadStatus {
  pending = "pending",
  error = "error",
  ready = "ready",
}

export type Upload = {
  index: number;
  id: number;
  filename: string;
  status: UploadStatus;
};
