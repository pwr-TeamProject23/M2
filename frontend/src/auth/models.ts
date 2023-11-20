export type LoginCredentials = {
  password: string;
  email: string;
};

export type User = {
  id: number;
  email: string;
  is_admin: boolean;
};
