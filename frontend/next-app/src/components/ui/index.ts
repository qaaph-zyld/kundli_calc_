/**
 * UI Design System
 * 
 * Central export file for all UI primitives.
 * Inspired by uiverse.io patterns with custom implementations.
 * All components are MIT licensed.
 */

// Design tokens (import this in your global CSS or layout)
import './design-tokens.css';

// Core components
export { default as Button } from './Button';
export type { ButtonProps, ButtonVariant, ButtonSize } from './Button';

export { default as Input } from './Input';
export type { InputProps, InputSize } from './Input';

export { default as Select } from './Select';
export type { SelectProps, SelectOption, SelectSize } from './Select';

export { Card, CardHeader, CardBody, CardFooter } from './Card';
export type { CardProps, CardHeaderProps, CardFooterProps, CardVariant, CardPadding } from './Card';

// Modal (to be added)
export { default as Modal } from './Modal';
export type { ModalProps } from './Modal';

// Tabs (to be added)
export { Tabs, TabList, Tab, TabPanels, TabPanel } from './Tabs';
export type { TabsProps, TabProps, TabPanelProps } from './Tabs';
