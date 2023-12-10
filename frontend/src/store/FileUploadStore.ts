import { create } from "zustand";

interface FileState {
  file: File | undefined;
  setFile: (file: File) => void;
  unsetFile: () => void;
  errorMessage: string | null;
  setErrorMessage: (errorMessage: string | null) => void;
}

export const useFileUploadStore = create<FileState>()((set) => ({
  file: undefined,
  setFile: (file: File) => set(() => ({ file: file })),
  unsetFile: () => set(() => ({ file: undefined, errorMessage: null })),
  errorMessage: null,
  setErrorMessage: (errorMessage: string | null) =>
    set((state) => ({
      errorMessage: errorMessage,
      file: errorMessage != null ? undefined : state.file,
    })),
}));
