import { create } from "zustand";
import { getLoggedUser } from "../auth/api";
import { User } from "../auth/models";

type AuthStore = {
  user: User | null;
  setUser: (user: User | null) => void;
  authenticate: () => Promise<void>;
};

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  setUser: (user) => set({ user: user }),
  authenticate: async () => {
    try {
      const user = await getLoggedUser();
      set({ user: user });
    } catch (e) {
      throw e;
    }
  },
}));
