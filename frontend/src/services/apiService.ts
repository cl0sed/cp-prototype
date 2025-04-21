// Add a basic logger for frontend
const logger = {
    info: (...args: any[]) => console.log('INFO:', ...args),
    warn: (...args: any[]) => console.warn('WARN:', ...args),
    error: (...args: any[]) => console.error('ERROR:', ...args),
};

// Base API service for handling HTTP requests

type RequestMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';

interface RequestOptions {
  method?: RequestMethod;
  headers?: HeadersInit;
  body?: any;
  credentials?: RequestCredentials;
}

// Define types for chat messages based on backend schemas (aligned with backend/app/api/routers/chat.py)
export interface ChatMessage {
  id: string; // UUID string
  session_id: string; // UUID string
  role: 'user' | 'assistant' | 'tool';
  content: string;
  timestamp: string; // ISO format string
  metadata: Record<string, any>;
}

export interface ChatHistoryResponse {
  messages: ChatMessage[];
}

export interface ChatMessageRequest {
  message: string;
  session_id?: string; // Optional UUID string
}

export interface ChatMessageAPIResponse {
  reply: string;
  session_id: string; // UUID string
  model?: string; // Add optional model property for debugging display
}

export interface GreetingResponse {
    greeting: string;
    // Potentially add user-specific info here, e.g., recent tasks summary
}

class ApiService {
  private baseUrl: string;

  constructor() {
    // Use VITE_API_BASE_URL as per architecture plan, default to /api if not set
    this.baseUrl = import.meta.env.VITE_API_BASE_URL || '/api';
  }


  async request<T>(endpoint: string, options: RequestOptions = {}): Promise<T | null> { // Allow null return
    const url = `${this.baseUrl}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;

    console.log(`API Request: ${options.method || 'GET'} ${url}`);
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
      console.log(`API Response received for ${url}`);
      const response = await fetch(url, requestOptions);
      console.log(`API Response received for ${url}`);

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
      console.error(`API Error for ${url}:`, error);
      console.error(`API Error for ${url}:`, error);
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

  /**
   * Sends a message to the new chat endpoint.
   * @param message The current message from the user.
   * @param sessionId Optional ID of the current chat session.
   * @returns The agent's response and the session ID.
   * @throws {ApiError} If the API call fails.
   */
  async sendMessage(message: string, sessionId?: string): Promise<ChatMessageAPIResponse> {
    logger.info('Sending chat message...');
    const requestBody: ChatMessageRequest = {
      message: message,
      session_id: sessionId, // Pass the optional session ID
    };
    // Use the existing post method to the new endpoint
    const response = await this.post<ChatMessageAPIResponse>('/chat/message', requestBody);
    logger.info('Chat message sent, response received.');

    if (response === null) {
       throw new ApiError("Received empty response from chat endpoint", 500, {});
    }

    return response;
  }

  /**
   * Fetches chat message history for the authenticated user.
   * @param sessionId Optional ID of the session to fetch history for.
   * @param limit Optional limit on the number of messages.
   * @returns A list of chat messages.
   * @throws {ApiError} If the API call fails.
   */
  /*
  async getChatHistory(sessionId?: string, limit?: number): Promise<ChatHistoryResponse> {
      // logger.info(`Fetching chat history for session: ${sessionId}, limit: ${limit}`);
      // const queryParams = new URLSearchParams();
      // if (sessionId) {
      //     queryParams.append('session_id', sessionId);
      // }
      // if (limit !== undefined) {
      //     queryParams.append('limit', limit.toString());
      // }
      // const endpoint = `/chat/history${queryParams.toString() ? `?${queryParams.toString()}` : ''}`;
      // const response = await this.get<ChatHistoryResponse>(endpoint);
      // logger.info('Chat history received.');

      // if (response === null) {
      //     // Depending on backend implementation, empty history might return 200 with empty list
      //     // or 404. Assuming 200 with empty list is handled by the type.
      //     // If 404 is expected for no history, handle it in the calling component.
      //     // For now, assume null means an unexpected empty response.
      //     throw new ApiError("Received unexpected empty response from chat history endpoint", 500, {});
      // }

      // return response

      return { messages: [] };
  }
  */

  /**
   * Fetches the dynamic greeting for the authenticated user.
   * @returns The greeting text.
   * @throws {ApiError} If the API call fails.
   */
  async getGreeting(): Promise<GreetingResponse> {
      logger.info('Fetching greeting...');
      const response = await this.get<GreetingResponse>('/chat/greeting');
      logger.info('Greeting received.');

      if (response === null) {
          throw new ApiError("Received empty response from greeting endpoint", 500, {});
      }

      return response;
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

// Export the methods directly for easier import in components
export const sendMessage = apiService.sendMessage.bind(apiService);
// export const getChatHistory = apiService.getChatHistory.bind(apiService); // Temporarily disabled for debugging
export const getGreeting = apiService.getGreeting.bind(apiService);
