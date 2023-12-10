export type LoginCredentials = {
  password: string;
  email: string;
};

export type User = {
  user_id: number;
  email: string;
  is_admin: boolean;
};
