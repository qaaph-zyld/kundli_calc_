/**
 * Button Component
 * 
 * Design inspiration: Modern glassmorphic buttons from uiverse.io
 * License: MIT (custom implementation)
 * 
 * Features:
 * - Multiple variants (primary, secondary, ghost, danger)
 * - Multiple sizes (sm, md, lg)
 * - Loading state with spinner
 * - Icon support (left/right)
 * - Full accessibility support
 */

"use client";

import React, { forwardRef } from 'react';
import styles from './Button.module.css';

export type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'danger' | 'success';
export type ButtonSize = 'sm' | 'md' | 'lg';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
  children: React.ReactNode;
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      isLoading = false,
      leftIcon,
      rightIcon,
      fullWidth = false,
      disabled,
      className = '',
      children,
      ...props
    },
    ref
  ) => {
    const buttonClasses = [
      styles.button,
      styles[variant],
      styles[size],
      fullWidth && styles.fullWidth,
      isLoading && styles.loading,
      className,
    ]
      .filter(Boolean)
      .join(' ');

    return (
      <button
        ref={ref}
        className={buttonClasses}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading && (
          <span className={styles.spinner}>
            <svg
              className={styles.spinnerIcon}
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className={styles.spinnerTrack}
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className={styles.spinnerHead}
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
          </span>
        )}
        {leftIcon && !isLoading && <span className={styles.leftIcon}>{leftIcon}</span>}
        <span className={styles.content}>{children}</span>
        {rightIcon && !isLoading && <span className={styles.rightIcon}>{rightIcon}</span>}
        <span className={styles.shine} aria-hidden="true" />
      </button>
    );
  }
);

Button.displayName = 'Button';

export default Button;
