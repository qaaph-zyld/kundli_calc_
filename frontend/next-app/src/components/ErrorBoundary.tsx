'use client';

import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error?: Error;
  errorInfo?: ErrorInfo;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    
    this.setState({
      error,
      errorInfo
    });

    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }
  }

  handleReset = () => {
    this.setState({ hasError: false, error: undefined, errorInfo: undefined });
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="error-boundary-container">
          <div className="error-boundary-content">
            <div className="error-icon">⚠️</div>
            <h2 className="error-title">Something went wrong</h2>
            <p className="error-message">
              {this.state.error?.message || 'An unexpected error occurred'}
            </p>
            
            {process.env.NODE_ENV === 'development' && this.state.errorInfo && (
              <details className="error-details">
                <summary>Error Details (Development Only)</summary>
                <pre className="error-stack">
                  {this.state.error?.stack}
                </pre>
                <pre className="error-component-stack">
                  {this.state.errorInfo.componentStack}
                </pre>
              </details>
            )}

            <div className="error-actions">
              <button 
                onClick={this.handleReset}
                className="btn-primary"
              >
                Try Again
              </button>
              <button 
                onClick={() => window.location.reload()}
                className="btn-secondary"
              >
                Reload Page
              </button>
            </div>
          </div>

          <style jsx>{`
            .error-boundary-container {
              min-height: 400px;
              display: flex;
              align-items: center;
              justify-content: center;
              padding: 2rem;
              background: linear-gradient(135deg, #fef3f3 0%, #fff5f5 100%);
            }

            .error-boundary-content {
              max-width: 600px;
              width: 100%;
              background: white;
              border-radius: 12px;
              padding: 2.5rem;
              box-shadow: 0 4px 20px rgba(220, 38, 38, 0.1);
              text-align: center;
            }

            .error-icon {
              font-size: 4rem;
              margin-bottom: 1rem;
              animation: pulse 2s infinite;
            }

            @keyframes pulse {
              0%, 100% { opacity: 1; }
              50% { opacity: 0.6; }
            }

            .error-title {
              font-size: 1.75rem;
              font-weight: 700;
              color: #dc2626;
              margin-bottom: 1rem;
            }

            .error-message {
              font-size: 1rem;
              color: #6b7280;
              margin-bottom: 1.5rem;
              line-height: 1.6;
            }

            .error-details {
              text-align: left;
              margin: 1.5rem 0;
              padding: 1rem;
              background: #f9fafb;
              border-radius: 8px;
              border: 1px solid #e5e7eb;
            }

            .error-details summary {
              cursor: pointer;
              font-weight: 600;
              color: #4b5563;
              margin-bottom: 0.5rem;
            }

            .error-stack,
            .error-component-stack {
              font-size: 0.75rem;
              color: #6b7280;
              overflow-x: auto;
              padding: 0.75rem;
              background: white;
              border-radius: 4px;
              margin-top: 0.5rem;
            }

            .error-actions {
              display: flex;
              gap: 1rem;
              justify-content: center;
              margin-top: 2rem;
            }

            .btn-primary,
            .btn-secondary {
              padding: 0.75rem 1.5rem;
              border-radius: 8px;
              font-weight: 600;
              font-size: 0.95rem;
              cursor: pointer;
              transition: all 0.2s;
              border: none;
            }

            .btn-primary {
              background: #dc2626;
              color: white;
            }

            .btn-primary:hover {
              background: #b91c1c;
              transform: translateY(-1px);
            }

            .btn-secondary {
              background: white;
              color: #4b5563;
              border: 1px solid #d1d5db;
            }

            .btn-secondary:hover {
              background: #f9fafb;
              border-color: #9ca3af;
            }
          `}</style>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
