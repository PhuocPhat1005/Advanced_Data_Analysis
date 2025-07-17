"use client";

import { usePathname } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
import clsx from "clsx";

// icons
import { BiAnalyse } from "react-icons/bi";
import { MdDataset } from "react-icons/md";

export default function Sidebar() {
  const pathname = usePathname();

  const navItems = [
    { label: "Dashboard", href: "/dashboard" , icon: BiAnalyse},
    { label: "Customized Datasets", href: "/automation", icon: MdDataset},
  ];

  return (
    <aside className="w-64 h-screen bg-white shadow-xl flex flex-col px-4 py-6">
      <Link href="/dashboard" className="mb-8 mx-auto">
        <Image
          src="/logo.svg"
          alt="Logo"
          width={200}
          height={200}
          className="rounded-xl"
        />
      </Link>
      <nav className="flex flex-col gap-2">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={clsx(
              "flex items-center gap-2 px-4 py-2 rounded-md hover:bg-blue-200 transition",
              pathname === item.href && "bg-blue-300 font-semibold"
            )}
          >
            <item.icon className="text-xl" />
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}