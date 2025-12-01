/**
 * Tabs Component
 * 
 * Design inspiration: Animated tab components from uiverse.io
 * License: MIT (custom implementation)
 * 
 * Features:
 * - Animated indicator
 * - Keyboard navigation
 * - Full accessibility support (ARIA tabs pattern)
 */

"use client";

import React, { createContext, useContext, useState, useId, useRef, useEffect } from 'react';
import styles from './Tabs.module.css';

// Context for tabs state
interface TabsContextValue {
  activeIndex: number;
  setActiveIndex: (index: number) => void;
  tabsId: string;
  variant: TabsVariant;
}

const TabsContext = createContext<TabsContextValue | null>(null);

const useTabsContext = () => {
  const context = useContext(TabsContext);
  if (!context) {
    throw new Error('Tab components must be used within a Tabs provider');
  }
  return context;
};

// Types
export type TabsVariant = 'default' | 'pills' | 'underline';

export interface TabsProps {
  defaultIndex?: number;
  index?: number;
  onChange?: (index: number) => void;
  variant?: TabsVariant;
  children: React.ReactNode;
  className?: string;
}

export interface TabListProps {
  children: React.ReactNode;
  className?: string;
}

export interface TabProps {
  children: React.ReactNode;
  disabled?: boolean;
  className?: string;
}

export interface TabPanelsProps {
  children: React.ReactNode;
  className?: string;
}

export interface TabPanelProps {
  children: React.ReactNode;
  className?: string;
}

// Main Tabs container
const Tabs: React.FC<TabsProps> = ({
  defaultIndex = 0,
  index,
  onChange,
  variant = 'default',
  children,
  className = '',
}) => {
  const [activeIndex, setActiveIndexState] = useState(index ?? defaultIndex);
  const tabsId = useId();

  const setActiveIndex = (newIndex: number) => {
    if (index === undefined) {
      setActiveIndexState(newIndex);
    }
    onChange?.(newIndex);
  };

  // Sync controlled index
  useEffect(() => {
    if (index !== undefined) {
      setActiveIndexState(index);
    }
  }, [index]);

  const contextValue: TabsContextValue = {
    activeIndex,
    setActiveIndex,
    tabsId,
    variant,
  };

  return (
    <TabsContext.Provider value={contextValue}>
      <div className={`${styles.tabs} ${className}`}>{children}</div>
    </TabsContext.Provider>
  );
};

// Tab list container
const TabList: React.FC<TabListProps> = ({ children, className = '' }) => {
  const { variant } = useTabsContext();
  const listRef = useRef<HTMLDivElement>(null);
  const [indicatorStyle, setIndicatorStyle] = useState<React.CSSProperties>({});

  const childrenArray = React.Children.toArray(children);
  const { activeIndex, setActiveIndex } = useTabsContext();

  // Update indicator position
  useEffect(() => {
    const list = listRef.current;
    if (!list) return;

    const tabs = list.querySelectorAll('[role="tab"]');
    const activeTab = tabs[activeIndex] as HTMLElement;

    if (activeTab) {
      setIndicatorStyle({
        left: activeTab.offsetLeft,
        width: activeTab.offsetWidth,
      });
    }
  }, [activeIndex]);

  // Keyboard navigation
  const handleKeyDown = (e: React.KeyboardEvent) => {
    const tabs = listRef.current?.querySelectorAll('[role="tab"]:not([disabled])');
    if (!tabs) return;

    const tabsArray = Array.from(tabs) as HTMLElement[];
    const currentIndex = tabsArray.findIndex(tab => tab === document.activeElement);

    let newIndex = currentIndex;

    switch (e.key) {
      case 'ArrowLeft':
        newIndex = currentIndex > 0 ? currentIndex - 1 : tabsArray.length - 1;
        e.preventDefault();
        break;
      case 'ArrowRight':
        newIndex = currentIndex < tabsArray.length - 1 ? currentIndex + 1 : 0;
        e.preventDefault();
        break;
      case 'Home':
        newIndex = 0;
        e.preventDefault();
        break;
      case 'End':
        newIndex = tabsArray.length - 1;
        e.preventDefault();
        break;
    }

    if (newIndex !== currentIndex) {
      tabsArray[newIndex]?.focus();
    }
  };

  return (
    <div
      ref={listRef}
      role="tablist"
      className={`${styles.tabList} ${styles[variant]} ${className}`}
      onKeyDown={handleKeyDown}
    >
      {React.Children.map(children, (child, index) => {
        if (React.isValidElement(child)) {
          return React.cloneElement(child as React.ReactElement<any>, { index });
        }
        return child;
      })}
      {variant !== 'pills' && (
        <span className={styles.indicator} style={indicatorStyle} aria-hidden="true" />
      )}
    </div>
  );
};

// Individual Tab button
const Tab: React.FC<TabProps & { index?: number }> = ({
  children,
  disabled = false,
  className = '',
  index = 0,
}) => {
  const { activeIndex, setActiveIndex, tabsId, variant } = useTabsContext();
  const isActive = activeIndex === index;

  const handleClick = () => {
    if (!disabled) {
      setActiveIndex(index);
    }
  };

  const tabClasses = [
    styles.tab,
    styles[variant],
    isActive && styles.active,
    disabled && styles.disabled,
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <button
      role="tab"
      type="button"
      id={`${tabsId}-tab-${index}`}
      aria-selected={isActive}
      aria-controls={`${tabsId}-panel-${index}`}
      aria-disabled={disabled}
      tabIndex={isActive ? 0 : -1}
      className={tabClasses}
      onClick={handleClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};

// Tab panels container
const TabPanels: React.FC<TabPanelsProps> = ({ children, className = '' }) => {
  const { activeIndex } = useTabsContext();

  return (
    <div className={`${styles.tabPanels} ${className}`}>
      {React.Children.map(children, (child, index) => {
        if (React.isValidElement(child) && index === activeIndex) {
          return React.cloneElement(child as React.ReactElement<any>, { index });
        }
        return null;
      })}
    </div>
  );
};

// Individual Tab panel
const TabPanel: React.FC<TabPanelProps & { index?: number }> = ({
  children,
  className = '',
  index = 0,
}) => {
  const { tabsId, activeIndex } = useTabsContext();
  const isActive = activeIndex === index;

  if (!isActive) return null;

  return (
    <div
      role="tabpanel"
      id={`${tabsId}-panel-${index}`}
      aria-labelledby={`${tabsId}-tab-${index}`}
      className={`${styles.tabPanel} ${className}`}
      tabIndex={0}
    >
      {children}
    </div>
  );
};

export { Tabs, TabList, Tab, TabPanels, TabPanel };
