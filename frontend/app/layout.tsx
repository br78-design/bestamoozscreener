import './globals.css';
import type { ReactNode } from 'react';

export const metadata = {
  title: 'bestamoozscreener',
  description: 'MVP بورس ایران - فیلترنویسی',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="fa" dir="rtl">
      <body className="bg-slate-50 text-slate-800">
        <div className="min-h-screen mx-auto max-w-6xl px-4 py-8">{children}</div>
      </body>
    </html>
  );
}
