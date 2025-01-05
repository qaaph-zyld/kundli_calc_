import React, { createContext, useContext, useState } from 'react';

interface AccessibilityContextType {
  fontSize: number;
  contrast: 'normal' | 'high';
  reducedMotion: boolean;
  screenReaderMode: boolean;
  setFontSize: (size: number) => void;
  setContrast: (contrast: 'normal' | 'high') => void;
  setReducedMotion: (reduced: boolean) => void;
  setScreenReaderMode: (enabled: boolean) => void;
}

const AccessibilityContext = createContext<AccessibilityContextType | undefined>(
  undefined
);

export const useAccessibility = () => {
  const context = useContext(AccessibilityContext);
  if (!context) {
    throw new Error(
      'useAccessibility must be used within an AccessibilityProvider'
    );
  }
  return context;
};

export const AccessibilityProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [fontSize, setFontSize] = useState(16);
  const [contrast, setContrast] = useState<'normal' | 'high'>('normal');
  const [reducedMotion, setReducedMotion] = useState(false);
  const [screenReaderMode, setScreenReaderMode] = useState(false);

  const value = {
    fontSize,
    contrast,
    reducedMotion,
    screenReaderMode,
    setFontSize,
    setContrast,
    setReducedMotion,
    setScreenReaderMode,
  };

  return (
    <AccessibilityContext.Provider value={value}>
      <div
        style={{
          fontSize: `${fontSize}px`,
          filter: contrast === 'high' ? 'contrast(1.5)' : 'none',
        }}
        className={`${reducedMotion ? 'reduce-motion' : ''} ${
          screenReaderMode ? 'screen-reader' : ''
        }`}
      >
        {children}
      </div>
    </AccessibilityContext.Provider>
  );
};
