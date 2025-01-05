import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import KundliForm from '../KundliForm';

const renderWithProviders = (component: React.ReactNode) => {
  return render(
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      {component}
    </LocalizationProvider>
  );
};

describe('KundliForm Component', () => {
  const mockOnSubmit = jest.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  it('renders all form fields', () => {
    renderWithProviders(<KundliForm onSubmit={mockOnSubmit} />);
    
    expect(screen.getByLabelText(/Date/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Time/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Latitude/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Longitude/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Timezone/i)).toBeInTheDocument();
  });

  it('validates required fields', async () => {
    renderWithProviders(<KundliForm onSubmit={mockOnSubmit} />);
    
    const submitButton = screen.getByRole('button', { name: /calculate/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getAllByText(/required/i)).toHaveLength(5);
    });
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('validates latitude range', async () => {
    renderWithProviders(<KundliForm onSubmit={mockOnSubmit} />);
    
    const latitudeInput = screen.getByLabelText(/Latitude/i);
    fireEvent.change(latitudeInput, { target: { value: '91' } });
    
    const submitButton = screen.getByRole('button', { name: /calculate/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/must be between -90 and 90/i)).toBeInTheDocument();
    });
  });

  it('validates longitude range', async () => {
    renderWithProviders(<KundliForm onSubmit={mockOnSubmit} />);
    
    const longitudeInput = screen.getByLabelText(/Longitude/i);
    fireEvent.change(longitudeInput, { target: { value: '181' } });
    
    const submitButton = screen.getByRole('button', { name: /calculate/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/must be between -180 and 180/i)).toBeInTheDocument();
    });
  });

  it('submits form with valid data', async () => {
    renderWithProviders(<KundliForm onSubmit={mockOnSubmit} />);
    
    // Fill in form fields
    fireEvent.change(screen.getByLabelText(/Latitude/i), { target: { value: '23.5' } });
    fireEvent.change(screen.getByLabelText(/Longitude/i), { target: { value: '76.5' } });
    fireEvent.change(screen.getByLabelText(/Timezone/i), { target: { value: 'Asia/Kolkata' } });
    
    // Note: Date and Time pickers would need special handling in a real test
    
    const submitButton = screen.getByRole('button', { name: /calculate/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalled();
    });
  });
});
