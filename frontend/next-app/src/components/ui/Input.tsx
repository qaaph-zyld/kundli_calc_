/**
 * Input Component
 * 
 * Design inspiration: Modern floating label inputs from uiverse.io
 * License: MIT (custom implementation)
 * 
 * Features:
 * - Floating label animation
 * - Error/success states
 * - Left/right icons
 * - Helper text
 * - Full accessibility support
 */

"use client";

import React, { forwardRef, useState, useId } from 'react';
import styles from './Input.module.css';

export type InputSize = 'sm' | 'md' | 'lg';

export interface InputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'> {
  label?: string;
  size?: InputSize;
  error?: string;
  success?: boolean;
  helperText?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      label,
      size = 'md',
      error,
      success,
      helperText,
      leftIcon,
      rightIcon,
      fullWidth = false,
      className = '',
      id,
      disabled,
      required,
      value,
      defaultValue,
      onFocus,
      onBlur,
      ...props
    },
    ref
  ) => {
    const generatedId = useId();
    const inputId = id || generatedId;
    const [isFocused, setIsFocused] = useState(false);
    const hasValue = value !== undefined ? Boolean(value) : Boolean(defaultValue);

    const handleFocus = (e: React.FocusEvent<HTMLInputElement>) => {
      setIsFocused(true);
      onFocus?.(e);
    };

    const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
      setIsFocused(false);
      onBlur?.(e);
    };

    const wrapperClasses = [
      styles.wrapper,
      styles[size],
      fullWidth && styles.fullWidth,
      error && styles.hasError,
      success && styles.hasSuccess,
      disabled && styles.disabled,
      isFocused && styles.focused,
      (hasValue || isFocused) && styles.hasValue,
      leftIcon && styles.hasLeftIcon,
      rightIcon && styles.hasRightIcon,
      className,
    ]
      .filter(Boolean)
      .join(' ');

    return (
      <div className={wrapperClasses}>
        <div className={styles.inputContainer}>
          {leftIcon && <span className={styles.leftIcon}>{leftIcon}</span>}
          
          <input
            ref={ref}
            id={inputId}
            className={styles.input}
            disabled={disabled}
            required={required}
            value={value}
            defaultValue={defaultValue}
            onFocus={handleFocus}
            onBlur={handleBlur}
            aria-invalid={!!error}
            aria-describedby={
              error ? `${inputId}-error` : helperText ? `${inputId}-helper` : undefined
            }
            {...props}
          />
          
          {label && (
            <label htmlFor={inputId} className={styles.label}>
              {label}
              {required && <span className={styles.required}>*</span>}
            </label>
          )}
          
          {rightIcon && <span className={styles.rightIcon}>{rightIcon}</span>}
          
          <span className={styles.border} aria-hidden="true" />
        </div>

        {(error || helperText) && (
          <span
            id={error ? `${inputId}-error` : `${inputId}-helper`}
            className={styles.helperText}
            role={error ? 'alert' : undefined}
          >
            {error || helperText}
          </span>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export default Input;
