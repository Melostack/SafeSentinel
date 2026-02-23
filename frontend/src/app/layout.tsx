import type { Metadata } from "next";
import { Space_Grotesk, Outfit } from "next/font/google";
import "./globals.css";

const spaceGrotesk = Space_Grotesk({ 
  subsets: ["latin"],
  variable: "--font-space-grotesk",
});

const outfit = Outfit({ 
  subsets: ["latin"],
  variable: "--font-outfit",
});

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
    <html lang="pt-br" className={`${spaceGrotesk.variable} ${outfit.variable}`}>
      <body className="antialiased font-sans bg-[#020202] text-white overflow-x-hidden">
        {children}
      </body>
    </html>
  );
}
