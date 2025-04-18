// Base API service for handling HTTP requests

type RequestMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';

interface RequestOptions {
  method?: RequestMethod;
  headers?: HeadersInit;
  body?: any;
  credentials?: RequestCredentials;
}

class ApiService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = import.meta.env.VITE_API_URL || '/api';
  }


  async request<T>(endpoint: string, options: RequestOptions = {}): Promise<T | null> { // Allow null return
    const url = `${this.baseUrl}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;

    const headers = new Headers(options.headers || {});
    headers.set('Content-Type', 'application/json');


    if (options.body && typeof options.body === 'object') {
      options.body = JSON.stringify(options.body);
    }

    const requestOptions: RequestInit = {
      method: options.method || 'GET',
      headers,
      credentials: options.credentials || 'include',
      ...(options.body ? { body: options.body } : {}),
    };

    try {
      const response = await fetch(url, requestOptions);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new ApiError(
          errorData.message || `Request failed with status ${response.status}`,
          response.status,
          errorData
        );
      }

      // Check if response is empty
      const text = await response.text();
      return text ? JSON.parse(text) : null; // Return null for empty response
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      throw new ApiError(
        error instanceof Error ? error.message : 'An unknown error occurred',
        0,
        {}
      );
    }
  }

  // Convenience methods
  async get<T>(endpoint: string, options: Omit<RequestOptions, 'method' | 'body'> = {}): Promise<T | null> {
    return this.request<T>(endpoint, { ...options, method: 'GET' });
  }

  async post<T>(endpoint: string, data?: any, options: Omit<RequestOptions, 'method'> = {}): Promise<T | null> {
    return this.request<T>(endpoint, { ...options, method: 'POST', body: data });
  }

  async put<T>(endpoint: string, data?: any, options: Omit<RequestOptions, 'method'> = {}): Promise<T | null> {
    return this.request<T>(endpoint, { ...options, method: 'PUT', body: data });
  }

  async delete<T>(endpoint: string, options: Omit<RequestOptions, 'method'> = {}): Promise<T | null> {
    return this.request<T>(endpoint, { ...options, method: 'DELETE' });
  }

  async patch<T>(endpoint: string, data?: any, options: Omit<RequestOptions, 'method'> = {}): Promise<T | null> {
    return this.request<T>(endpoint, { ...options, method: 'PATCH', body: data });
  }
}

// Custom error class for API errors
export class ApiError extends Error {
  status: number;
  data: any;

  constructor(message: string, status: number, data: any) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.data = data;
  }
}

// Create and export singleton instance
export const apiService = new ApiService();
