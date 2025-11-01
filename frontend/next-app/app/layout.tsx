import type { ReactNode } from 'react';
export const metadata = {
  title: 'Kundli Calc',
  description: 'World-class Kundli calculations',
};

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en">
      <body style={{ fontFamily: 'system-ui, -apple-system, Segoe UI, Roboto, sans-serif', margin: 0 }}>
        {children}
      </body>
    </html>
  );
}
