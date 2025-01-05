import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme, CssBaseline, CircularProgress, Box, Typography } from '@mui/material';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import ErrorBoundary from './components/error/ErrorBoundary';
import { AccessibilityProvider } from './components/common/AccessibilityProvider';

// Lazy load components
const Layout = lazy(() => import('./components/layout/Layout'));
const Home = lazy(() => import('./pages/Home'));
const Login = lazy(() => import('./pages/Login'));
const KundliForm = lazy(() => import('./components/forms/KundliForm'));
const PredictionsPage = lazy(() => import('./pages/Predictions'));
const MatchingPage = lazy(() => import('./pages/Matching'));
const TransitPage = lazy(() => import('./pages/Transit'));
const { AuthProvider } = lazy(() => import('./contexts/AuthContext'));
const ProtectedRoute = lazy(() => import('./components/auth/ProtectedRoute'));

// Loading component
const LoadingFallback = () => (
  <Box
    sx={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '100vh',
    }}
    role="progressbar"
    aria-label="Loading application"
  >
    <CircularProgress />
  </Box>
);

// Create theme instance
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),
  },
  components: {
    MuiButton: {
      defaultProps: {
        // Add aria-label to buttons without text
        'aria-label': 'button',
      },
    },
    MuiIconButton: {
      defaultProps: {
        // Add aria-label to icon buttons
        'aria-label': 'button',
      },
    },
  },
});

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <AccessibilityProvider>
          <LocalizationProvider dateAdapter={AdapterDateFns}>
            <Suspense fallback={<LoadingFallback />}>
              <AuthProvider>
                <Router>
                  <Layout>
                    <ErrorBoundary>
                      <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/login" element={<Login />} />
                        <Route
                          path="/calculate"
                          element={
                            <ProtectedRoute>
                              <KundliForm />
                            </ProtectedRoute>
                          }
                        />
                        <Route
                          path="/predictions"
                          element={
                            <ProtectedRoute requiredRole="premium">
                              <PredictionsPage />
                            </ProtectedRoute>
                          }
                        />
                        <Route
                          path="/matching"
                          element={
                            <ProtectedRoute requiredRole="premium">
                              <MatchingPage />
                            </ProtectedRoute>
                          }
                        />
                        <Route
                          path="/transit"
                          element={
                            <ProtectedRoute requiredRole="premium">
                              <TransitPage />
                            </ProtectedRoute>
                          }
                        />
                        <Route
                          path="*"
                          element={
                            <Box
                              sx={{
                                display: 'flex',
                                justifyContent: 'center',
                                alignItems: 'center',
                                minHeight: '60vh',
                              }}
                              role="alert"
                            >
                              <Typography variant="h4">
                                404 - Page Not Found
                              </Typography>
                            </Box>
                          }
                        />
                      </Routes>
                    </ErrorBoundary>
                  </Layout>
                </Router>
              </AuthProvider>
            </Suspense>
          </LocalizationProvider>
        </AccessibilityProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
