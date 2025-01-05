import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { kundliApi, KundliRequest } from '../../services/api';

interface KundliState {
  currentKundli: any | null;
  predictions: any[];
  loading: boolean;
  error: string | null;
  savedKundlis: any[];
}

const initialState: KundliState = {
  currentKundli: null,
  predictions: [],
  loading: false,
  error: null,
  savedKundlis: [],
};

export const calculateKundli = createAsyncThunk(
  'kundli/calculate',
  async (data: KundliRequest) => {
    const response = await kundliApi.calculate(data);
    return response;
  }
);

export const generatePredictions = createAsyncThunk(
  'kundli/predictions',
  async (id: string) => {
    const response = await kundliApi.generatePredictions(id);
    return response;
  }
);

const kundliSlice = createSlice({
  name: 'kundli',
  initialState,
  reducers: {
    clearCurrentKundli: (state) => {
      state.currentKundli = null;
      state.predictions = [];
    },
    saveKundli: (state, action) => {
      state.savedKundlis.push(action.payload);
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(calculateKundli.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(calculateKundli.fulfilled, (state, action) => {
        state.loading = false;
        state.currentKundli = action.payload;
      })
      .addCase(calculateKundli.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to calculate kundli';
      })
      .addCase(generatePredictions.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(generatePredictions.fulfilled, (state, action) => {
        state.loading = false;
        state.predictions = action.payload;
      })
      .addCase(generatePredictions.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to generate predictions';
      });
  },
});

export const { clearCurrentKundli, saveKundli } = kundliSlice.actions;
export default kundliSlice.reducer;
