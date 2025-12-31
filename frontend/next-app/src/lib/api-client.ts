import axios, { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export interface ApiError {
  message: string;
  code?: string;
  status?: number;
  details?: any;
  userFriendlyMessage: string;
}

export class ApiClient {
  private client: AxiosInstance;
  private requestCache: Map<string, { data: any; timestamp: number }> = new Map();
  private cacheDuration = 5 * 60 * 1000;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    this.client.interceptors.request.use(
      (config) => {
        const token = this.getAuthToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(this.handleError(error))
    );

    this.client.interceptors.response.use(
      (response) => response,
      (error) => Promise.reject(this.handleError(error))
    );
  }

  private getAuthToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('auth_token');
    }
    return null;
  }

  private handleError(error: AxiosError): ApiError {
    const apiError: ApiError = {
      message: 'An unexpected error occurred',
      userFriendlyMessage: 'Something went wrong. Please try again.',
      status: error.response?.status,
    };

    if (error.response) {
      const status = error.response.status;
      const data: any = error.response.data;

      apiError.message = data?.message || data?.detail || error.message;
      apiError.code = data?.code;
      apiError.details = data?.details;

      switch (status) {
        case 400:
          apiError.userFriendlyMessage = 'Invalid input. Please check your data and try again.';
          break;
        case 401:
          apiError.userFriendlyMessage = 'You need to be logged in to access this feature.';
          break;
        case 403:
          apiError.userFriendlyMessage = 'You don\'t have permission to perform this action.';
          break;
        case 404:
          apiError.userFriendlyMessage = 'The requested resource was not found.';
          break;
        case 422:
          apiError.userFriendlyMessage = 'Validation error. Please check your input.';
          if (data?.detail) {
            const validationErrors = Array.isArray(data.detail) 
              ? data.detail.map((err: any) => err.msg).join(', ')
              : data.detail;
            apiError.userFriendlyMessage = `Validation error: ${validationErrors}`;
          }
          break;
        case 429:
          apiError.userFriendlyMessage = 'Too many requests. Please wait a moment and try again.';
          break;
        case 500:
          apiError.userFriendlyMessage = 'Server error. Our team has been notified.';
          break;
        case 503:
          apiError.userFriendlyMessage = 'Service temporarily unavailable. Please try again later.';
          break;
        default:
          apiError.userFriendlyMessage = `Error ${status}: ${apiError.message}`;
      }
    } else if (error.request) {
      apiError.message = 'No response from server';
      apiError.userFriendlyMessage = 'Unable to connect to the server. Please check your internet connection.';
    } else {
      apiError.message = error.message;
      apiError.userFriendlyMessage = 'An unexpected error occurred. Please try again.';
    }

    console.error('API Error:', apiError);
    return apiError;
  }

  private getCacheKey(url: string, params?: any): string {
    return `${url}:${JSON.stringify(params ?? {})}`;
  }

  private getFromCache(cacheKey: string): any | null {
    const cached = this.requestCache.get(cacheKey);
    if (cached && Date.now() - cached.timestamp < this.cacheDuration) {
      return cached.data;
    }
    this.requestCache.delete(cacheKey);
    return null;
  }

  private setCache(cacheKey: string, data: any) {
    this.requestCache.set(cacheKey, {
      data,
      timestamp: Date.now(),
    });

    if (this.requestCache.size > 100) {
      const firstKey = this.requestCache.keys().next().value;
      this.requestCache.delete(firstKey);
    }
  }

  public clearCache() {
    this.requestCache.clear();
  }

  async get<T = any>(
    url: string,
    config?: AxiosRequestConfig & { useCache?: boolean }
  ): Promise<T> {
    const { useCache = true, ...axiosConfig } = config || {};
    
    if (useCache) {
      const cacheKey = this.getCacheKey(url, axiosConfig.params);
      const cached = this.getFromCache(cacheKey);
      if (cached) {
        return cached as T;
      }

      const response = await this.client.get<T>(url, axiosConfig);
      this.setCache(cacheKey, response.data);
      return response.data;
    }

    const response = await this.client.get<T>(url, axiosConfig);
    return response.data;
  }

  async post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.post<T>(url, data, config);
    return response.data;
  }

  async put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.put<T>(url, data, config);
    return response.data;
  }

  async delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.delete<T>(url, config);
    return response.data;
  }

  async patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.patch<T>(url, data, config);
    return response.data;
  }
}

export const apiClient = new ApiClient();

export default apiClient;
