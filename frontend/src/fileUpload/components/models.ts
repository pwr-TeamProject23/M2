export enum SearchStatus {
  pending = "pending",
  error = "error",
  ready = "ready",
}

export type Search = {
  index: number;
  id: number;
  filename: string;
  status: SearchStatus;
};
