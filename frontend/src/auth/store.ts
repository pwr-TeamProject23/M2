import { create } from "zustand";
import { getLoggedUser } from "./api";
import { User } from "./models";

type AuthStore = {
  user: User | null;
  setUser: (user: User | null) => void;
  authenticate: () => Promise<void>;
};

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  authenticate: async () => {
    try {
      const user = await getLoggedUser();
      set({ user });
    } catch (e) {
      throw e;
    }
  },
}));
