import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from '../../../contexts/AuthContext';
import Header from '../Header';

const renderWithProviders = (component: React.ReactNode) => {
  return render(
    <BrowserRouter>
      <AuthProvider>{component}</AuthProvider>
    </BrowserRouter>
  );
};

describe('Header Component', () => {
  it('renders logo and navigation links', () => {
    renderWithProviders(<Header />);
    
    expect(screen.getByText(/Kundli/i)).toBeInTheDocument();
    expect(screen.getByText(/Home/i)).toBeInTheDocument();
    expect(screen.getByText(/Calculate/i)).toBeInTheDocument();
  });

  it('shows login button when user is not authenticated', () => {
    renderWithProviders(<Header />);
    
    expect(screen.getByText(/Login/i)).toBeInTheDocument();
    expect(screen.queryByText(/Logout/i)).not.toBeInTheDocument();
  });

  it('shows premium features when user has premium role', () => {
    // Mock the useAuth hook to return a premium user
    jest.spyOn(require('../../../contexts/AuthContext'), 'useAuth').mockImplementation(() => ({
      user: { role: 'premium' },
      loading: false,
    }));

    renderWithProviders(<Header />);
    
    expect(screen.getByText(/Predictions/i)).toBeInTheDocument();
    expect(screen.getByText(/Matching/i)).toBeInTheDocument();
    expect(screen.getByText(/Transit/i)).toBeInTheDocument();
  });
});
