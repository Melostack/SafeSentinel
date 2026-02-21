import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SafeSentinel | MarIA Strategy",
  description: "Web3 Interpretive Security Layer powered by Oratech",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-br">
      <body className="antialiased">{children}</body>
    </html>
  );
}
