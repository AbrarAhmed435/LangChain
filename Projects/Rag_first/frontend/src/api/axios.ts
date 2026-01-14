import axios from "axios";
import type {
  AxiosError,
  InternalAxiosRequestConfig,
} from "axios";
import {
  getAccessToken,
  getRefreshToken,
  setAccessToken,
  clearTokens,
} from "../utils/token";
import { refreshTokenApi } from "./auth.api";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

/* ================= REQUEST ================= */
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = getAccessToken();

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  }
);

/* ================= RESPONSE ================= */
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as
      | (InternalAxiosRequestConfig & { _retry?: boolean })
      | undefined;

    // Access token expired
    if (
      error.response?.status === 401 &&
      originalRequest &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      const refresh = getRefreshToken();

      if (!refresh) {
        clearTokens();
        window.location.href = "/login";
        return Promise.reject(error);
      }

      try {
        const res = await refreshTokenApi(refresh);
        setAccessToken(res.access);

        originalRequest.headers.Authorization =
          `Bearer ${res.access}`;

        return api(originalRequest); // retry request
      } catch (refreshError) {
        clearTokens();
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
