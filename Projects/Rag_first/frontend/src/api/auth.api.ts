import api from "./axios";
import type {
  LoginRequest,
  RegisterRequest,
  AuthResponse,
} from "../types/auth";

// LOGIN
export const loginApi = async (
  data: LoginRequest
): Promise<AuthResponse> => {
  const response = await api.post<AuthResponse>(
    "/login/",
    data
  );
  return response.data;
};

// REGISTER
export const registerApi = async (
  data: RegisterRequest
): Promise<AuthResponse> => {
  const response = await api.post<AuthResponse>(
    "/register/",
    data
  );
  return response.data;
};


export const refreshTokenApi = async (
  refresh: string
): Promise<{ access: string }> => {
  const res = await api.post<{ access: string }>(
    "/token/refresh/",
    { refresh }
  );
  return res.data;
};
