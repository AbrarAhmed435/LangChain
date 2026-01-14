export const getAccessToken = (): string | null =>
  localStorage.getItem("access");

export const getRefreshToken = (): string | null =>
  localStorage.getItem("refresh");

export const setAccessToken = (token: string) => {
  localStorage.setItem("access", token);
};

export const clearTokens = () => {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
};
