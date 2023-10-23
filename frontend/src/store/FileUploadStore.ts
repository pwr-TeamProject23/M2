import { create } from "zustand";

interface FileState {
  file: File | undefined;
  setFile: (file: File) => void;
}

export const useFileUploadStore = create<FileState>()((set) => ({
  file: undefined,
  setFile: (file: File) => set(() => ({ file: file })),
}));
