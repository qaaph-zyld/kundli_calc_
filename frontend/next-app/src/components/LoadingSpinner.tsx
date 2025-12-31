'use client';

import React from 'react';

interface LoadingSpinnerProps {
  size?: 'small' | 'medium' | 'large';
  message?: string;
  fullScreen?: boolean;
  variant?: 'default' | 'chart' | 'calculation';
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'medium',
  message,
  fullScreen = false,
  variant = 'default'
}) => {
  const sizeClasses = {
    small: 'w-6 h-6',
    medium: 'w-12 h-12',
    large: 'w-16 h-16'
  };

  const renderSpinner = () => {
    if (variant === 'chart') {
      return (
        <div className="chart-loader">
          <div className="chart-loader-circle"></div>
          <div className="chart-loader-planets">
            <div className="planet planet-1">☉</div>
            <div className="planet planet-2">☽</div>
            <div className="planet planet-3">♂</div>
          </div>
        </div>
      );
    }

    if (variant === 'calculation') {
      return (
        <div className="calculation-loader">
          <div className="calc-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <div className="calc-text">Calculating...</div>
        </div>
      );
    }

    return (
      <svg
        className={`spinner ${sizeClasses[size]}`}
        viewBox="0 0 50 50"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle
          className="spinner-circle"
          cx="25"
          cy="25"
          r="20"
          fill="none"
          strokeWidth="4"
        />
      </svg>
    );
  };

  const content = (
    <div className={`loading-container ${fullScreen ? 'fullscreen' : ''}`}>
      <div className="loading-content">
        {renderSpinner()}
        {message && <p className="loading-message">{message}</p>}
      </div>

      <style jsx>{`
        .loading-container {
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 2rem;
        }

        .loading-container.fullscreen {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(255, 255, 255, 0.95);
          z-index: 9999;
        }

        .loading-content {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 1rem;
        }

        .spinner {
          animation: rotate 2s linear infinite;
        }

        .spinner-circle {
          stroke: #8b5cf6;
          stroke-linecap: round;
          stroke-dasharray: 1, 150;
          stroke-dashoffset: 0;
          animation: dash 1.5s ease-in-out infinite;
        }

        @keyframes rotate {
          100% {
            transform: rotate(360deg);
          }
        }

        @keyframes dash {
          0% {
            stroke-dasharray: 1, 150;
            stroke-dashoffset: 0;
          }
          50% {
            stroke-dasharray: 90, 150;
            stroke-dashoffset: -35;
          }
          100% {
            stroke-dasharray: 90, 150;
            stroke-dashoffset: -124;
          }
        }

        .chart-loader {
          position: relative;
          width: 80px;
          height: 80px;
        }

        .chart-loader-circle {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          border: 3px solid #e5e7eb;
          border-top-color: #8b5cf6;
          border-radius: 50%;
          animation: spin 1.5s linear infinite;
        }

        .chart-loader-planets {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
        }

        .planet {
          position: absolute;
          font-size: 1.25rem;
          animation: orbit 3s linear infinite;
        }

        .planet-1 {
          animation-delay: 0s;
        }

        .planet-2 {
          animation-delay: 1s;
        }

        .planet-3 {
          animation-delay: 2s;
        }

        @keyframes spin {
          to {
            transform: rotate(360deg);
          }
        }

        @keyframes orbit {
          0%, 100% {
            transform: translate(-50%, -50%) scale(0.8);
            opacity: 0.3;
          }
          50% {
            transform: translate(-50%, -50%) scale(1.2);
            opacity: 1;
          }
        }

        .calculation-loader {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 1rem;
        }

        .calc-dots {
          display: flex;
          gap: 0.5rem;
        }

        .calc-dots span {
          width: 12px;
          height: 12px;
          border-radius: 50%;
          background: #8b5cf6;
          animation: bounce 1.4s infinite ease-in-out both;
        }

        .calc-dots span:nth-child(1) {
          animation-delay: -0.32s;
        }

        .calc-dots span:nth-child(2) {
          animation-delay: -0.16s;
        }

        @keyframes bounce {
          0%, 80%, 100% {
            transform: scale(0);
          }
          40% {
            transform: scale(1);
          }
        }

        .calc-text {
          font-size: 0.875rem;
          color: #6b7280;
          font-weight: 500;
        }

        .loading-message {
          font-size: 0.95rem;
          color: #6b7280;
          font-weight: 500;
          text-align: center;
          max-width: 300px;
        }
      `}</style>
    </div>
  );

  return content;
};

export default LoadingSpinner;
