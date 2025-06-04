import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { Toaster } from "../components/ui/toaster";
import { ThemeProvider } from "../components/theme-provider";
import "../styles/globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "프롬프트 생성기",
  description: "모델 최적화 프롬프트 생성기",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          {children}
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  );
}
