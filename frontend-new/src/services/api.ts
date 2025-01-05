import axios from 'axios';
import { trackAPIPerformance } from '../utils/performance';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for authentication
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export interface KundliRequest {
  date: string;
  time: string;
  latitude: number;
  longitude: number;
  timezone: string;
  ayanamsa: string;
  houseSystem: string;
  chartTypes?: string[];
  calculationType?: string;
  language?: string;
}

export interface TransitRequest extends KundliRequest {
  transitDate: string;
  transitTime: string;
}

export interface MatchingRequest {
  person1: KundliRequest;
  person2: KundliRequest;
  matchFactors?: string[];
}

export const kundliApi = {
  calculate: async (data: KundliRequest) => {
    return trackAPIPerformance(
      async () => {
        const response = await api.post('/api/kundli/calculate', data);
        return response.data;
      },
      'kundli_calculate'
    );
  },

  getById: async (id: string) => {
    return trackAPIPerformance(
      async () => {
        const response = await api.get(`/api/kundli/${id}`);
        return response.data;
      },
      'kundli_get'
    );
  },

  calculateTransit: async (data: TransitRequest) => {
    return trackAPIPerformance(
      async () => {
        const response = await api.post('/api/kundli/transit', data);
        return response.data;
      },
      'kundli_transit'
    );
  },

  calculateMatching: async (data: MatchingRequest) => {
    return trackAPIPerformance(
      async () => {
        const response = await api.post('/api/kundli/match', data);
        return response.data;
      },
      'kundli_match'
    );
  },

  generatePredictions: async (id: string, options?: any) => {
    return trackAPIPerformance(
      async () => {
        const response = await api.post(`/api/kundli/${id}/predict`, options);
        return response.data;
      },
      'kundli_predict'
    );
  },
};

export const authApi = {
  login: async (credentials: { username: string; password: string }) => {
    return trackAPIPerformance(
      async () => {
        const response = await api.post('/api/auth/login', credentials);
        return response.data;
      },
      'auth_login'
    );
  },

  register: async (userData: {
    username: string;
    password: string;
    email: string;
  }) => {
    return trackAPIPerformance(
      async () => {
        const response = await api.post('/api/auth/register', userData);
        return response.data;
      },
      'auth_register'
    );
  },

  refreshToken: async () => {
    return trackAPIPerformance(
      async () => {
        const response = await api.post('/api/auth/refresh');
        return response.data;
      },
      'auth_refresh'
    );
  },
};

export default api;
