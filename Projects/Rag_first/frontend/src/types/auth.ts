// -------- REQUEST TYPES --------

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  confirm_password: string;
}

// -------- RESPONSE TYPES --------

export interface AuthResponse {
  access: string;
  refresh: string;
}
