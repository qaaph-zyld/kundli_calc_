import type { ReactNode } from 'react';
import { AuthProvider } from '../src/contexts/AuthContext';
import './globals.css';

export const metadata = {
  title: 'Kundli Calculator - Vedic Astrology Charts',
  description: 'Generate accurate Vedic astrology birth charts with South Indian and Navamsa chart styles',
};

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
