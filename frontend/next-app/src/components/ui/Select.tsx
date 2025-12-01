/**
 * Select Component
 * 
 * Design inspiration: Custom styled selects from uiverse.io
 * License: MIT (custom implementation)
 * 
 * Features:
 * - Floating label
 * - Custom chevron icon
 * - Error/success states
 * - Full accessibility support
 */

"use client";

import React, { forwardRef, useState, useId } from 'react';
import styles from './Select.module.css';

export type SelectSize = 'sm' | 'md' | 'lg';

export interface SelectOption {
  value: string;
  label: string;
  disabled?: boolean;
}

export interface SelectProps extends Omit<React.SelectHTMLAttributes<HTMLSelectElement>, 'size'> {
  label?: string;
  size?: SelectSize;
  options: SelectOption[];
  placeholder?: string;
  error?: string;
  success?: boolean;
  helperText?: string;
  fullWidth?: boolean;
}

const Select = forwardRef<HTMLSelectElement, SelectProps>(
  (
    {
      label,
      size = 'md',
      options,
      placeholder = 'Select an option',
      error,
      success,
      helperText,
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
    const selectId = id || generatedId;
    const [isFocused, setIsFocused] = useState(false);
    const hasValue = value !== undefined ? Boolean(value) : Boolean(defaultValue);

    const handleFocus = (e: React.FocusEvent<HTMLSelectElement>) => {
      setIsFocused(true);
      onFocus?.(e);
    };

    const handleBlur = (e: React.FocusEvent<HTMLSelectElement>) => {
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
      hasValue && styles.hasValue,
      className,
    ]
      .filter(Boolean)
      .join(' ');

    return (
      <div className={wrapperClasses}>
        <div className={styles.selectContainer}>
          <select
            ref={ref}
            id={selectId}
            className={styles.select}
            disabled={disabled}
            required={required}
            value={value}
            defaultValue={defaultValue}
            onFocus={handleFocus}
            onBlur={handleBlur}
            aria-invalid={!!error}
            aria-describedby={
              error ? `${selectId}-error` : helperText ? `${selectId}-helper` : undefined
            }
            {...props}
          >
            <option value="" disabled hidden>
              {placeholder}
            </option>
            {options.map((option) => (
              <option
                key={option.value}
                value={option.value}
                disabled={option.disabled}
              >
                {option.label}
              </option>
            ))}
          </select>
          
          {label && (
            <label htmlFor={selectId} className={styles.label}>
              {label}
              {required && <span className={styles.required}>*</span>}
            </label>
          )}
          
          <span className={styles.chevron} aria-hidden="true">
            <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
              <path
                d="M2.5 4.5L6 8L9.5 4.5"
                stroke="currentColor"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </span>
          
          <span className={styles.border} aria-hidden="true" />
        </div>

        {(error || helperText) && (
          <span
            id={error ? `${selectId}-error` : `${selectId}-helper`}
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

Select.displayName = 'Select';

export default Select;
