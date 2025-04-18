import { apiService } from './apiService';

// Types
export interface UserCredentials {
  email: string;
  password: string;
  username?: string; // Optional for signup
}

export interface UserData {
  id: string;
  email: string;
  username: string;
  // Add any other user fields as needed
}

export interface AuthResponse {
  token: string;
  user: UserData;
}

// Authentication API endpoints
const AUTH_ENDPOINTS = {
  LOGIN: '/auth/login',
  SIGNUP: '/auth/signup',
  LOGOUT: '/auth/logout',
  USER_PROFILE: '/auth/me',
};

/**
 * Login user with email and password
 */
export const loginUser = async (credentials: UserCredentials): Promise<AuthResponse> => {
  try {
    return await apiService.post<AuthResponse>(AUTH_ENDPOINTS.LOGIN, credentials);
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};

/**
 * Register a new user
 */
export const signupUser = async (credentials: UserCredentials): Promise<AuthResponse> => {
  if (!credentials.username) {
    throw new Error('Username is required for signup');
  }

  try {
    return await apiService.post<AuthResponse>(AUTH_ENDPOINTS.SIGNUP, credentials);
  } catch (error) {
    console.error('Signup error:', error);
    throw error;
  }
};

/**
 * Fetch current user profile
 */
export const getUserProfile = async (): Promise<UserData> => {
  try {
    return await apiService.get<UserData>(AUTH_ENDPOINTS.USER_PROFILE);
  } catch (error) {
    console.error('Get user profile error:', error);
    throw error;
  }
};
