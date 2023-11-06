import { create } from "zustand";

interface FileState {
  file: File | undefined;
  setFile: (file: File) => void;
  unsetFile: () => void;
}

export const useFileUploadStore = create<FileState>()((set) => ({
  file: undefined,
  setFile: (file: File) => set(() => ({ file: file })),
  unsetFile: () => set(() => ({ file: undefined })),
}));
