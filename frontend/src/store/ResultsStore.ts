import { create } from "zustand";
import { Author } from "../articleSummary/models";

interface SuggestionsState {
  suggestions: Author[] | undefined;
  setSuggestions: (results: Author[]) => void;
}

export const useSuggestionsStore = create<SuggestionsState>()((set) => ({
  suggestions: undefined,
  setSuggestions: (suggestions: Author[]) =>
    set(() => ({ suggestions: suggestions })),
}));
