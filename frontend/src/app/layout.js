import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Sidebar from "@/components/sidebar";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "Advanced DA Project",
  description: "",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="flex antialiased">
        <Sidebar />
        <main className="flex-1 p-6">{children}</main>
      </body>
    </html>
  );
}