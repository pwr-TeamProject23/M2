import { create } from "zustand";
import { Search } from "./components/models";

type HistoryStore = {
  searches: Search[];
  setSearches: (s: Search[]) => void;
};

export const useHistoryStore = create<HistoryStore>((set) => ({
  searches: [],
  setSearches: (searches: Search[]) => set({ searches }),
}));
