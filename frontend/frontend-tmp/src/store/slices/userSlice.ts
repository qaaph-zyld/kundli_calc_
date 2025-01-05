import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { authApi } from '../../services/api';

interface UserState {
  data: {
    id: string | null;
    username: string | null;
    email: string | null;
    role: string | null;
    lastLoginDate?: Date;
  };
  loading: boolean;
  error: string | null;
}

const initialState: UserState = {
  data: {
    id: null,
    username: null,
    email: null,
    role: null,
  },
  loading: false,
  error: null,
};

export const loginUser = createAsyncThunk(
  'user/login',
  async (credentials: { username: string; password: string }) => {
    const response = await authApi.login(credentials);
    return response;
  }
);

export const registerUser = createAsyncThunk(
  'user/register',
  async (userData: { username: string; password: string; email: string }) => {
    const response = await authApi.register(userData);
    return response;
  }
);

export const refreshToken = createAsyncThunk('user/refresh', async () => {
  const response = await authApi.refreshToken();
  return response;
});

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    logout: (state) => {
      state.data = initialState.data;
      localStorage.removeItem('token');
    },
    setUser: (state, action) => {
      state.data = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loginUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.loading = false;
        state.data = action.payload.user;
        localStorage.setItem('token', action.payload.token);
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Login failed';
      })
      .addCase(registerUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(registerUser.fulfilled, (state, action) => {
        state.loading = false;
        state.data = action.payload.user;
        localStorage.setItem('token', action.payload.token);
      })
      .addCase(registerUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Registration failed';
      })
      .addCase(refreshToken.fulfilled, (state, action) => {
        state.data = action.payload.user;
        localStorage.setItem('token', action.payload.token);
      });
  },
});

export const { logout, setUser } = userSlice.actions;
export default userSlice.reducer;
