"use client";

import { usePathname } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
import clsx from "clsx";

import { RiMoneyDollarBoxFill } from "react-icons/ri";
import { MdDataset, MdOutlineBugReport, MdOutlineReviews } from "react-icons/md";
import { IoChatbubbleOutline } from "react-icons/io5";
import { BiBarChartAlt2 } from "react-icons/bi";
import { FaLightbulb } from "react-icons/fa";
import { PiRobot } from "react-icons/pi";
import { GrStatusGood } from "react-icons/gr";

export default function Sidebar() {
  const pathname = usePathname();

  const groupedNavItems = [
    {
      section: "Tổng quan",
      items: [
        { label: "Số lượng bán", href: "/sales", icon: BiBarChartAlt2 },
        { label: "Doanh thu", href: "/revenue", icon: RiMoneyDollarBoxFill },
        { label: "Status", href: "/status", icon: GrStatusGood},
        { label: "Reviews", href: "/review", icon: IoChatbubbleOutline },
      ],
    },
    {
      section: "phân tích nguyên nhân",
      items: [
        { label: "Trưng bày chết", href: "/dead-display", icon: MdOutlineBugReport },
        { label: "Review kém", href: "/bad-reviews", icon: MdOutlineReviews },
      ],
    },
    {
      section: "Gợi ý sản phẩm",
      items: [
        { label: "Kết quả gợi ý", href: "/recommendations", icon: FaLightbulb },
        { label: "Tuỳ chỉnh", href: "/customize", icon: MdDataset },
      ],
    },
    {
      section: "Hỗ trợ",
      items: [
        {label: "Chatbot", href: "/assistant", icon: PiRobot},
      ],
    },
  ];
  
  return (
    <aside className="w-64 h-screen bg-white shadow-xl flex flex-col px-4 py-6">
      <Link href="/overview" className="mb-8 mx-auto">
        <Image
          src="/logo.svg"
          alt="Logo"
          width={150}
          height={150}
          className="rounded-xl"
        />
      </Link>

      <nav className="flex flex-col gap-4 overflow-y-auto">
        {groupedNavItems.map((group) => (
          <div key={group.section}>
            <span className="text-xs text-gray-400 uppercase px-4 mb-1 block tracking-wide font-bold">
              {group.section}
            </span>
            <div className="flex flex-col gap-1">
              {group.items.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className={clsx(
                    "w-full flex items-center gap-3 px-4 py-2 rounded-lg transition-colors duration-300 ease-in-out active:scale-[0.98]",
                    pathname === item.href
                      ? "bg-blue-100 text-blue-800 font-semibold shadow-inner border-l-4 border-blue-500"
                      : "hover:bg-blue-50 hover:text-blue-700 text-gray-700"
                  )}
                >
                  <item.icon className="text-xl shrink-0" />
                  <span className="truncate">{item.label}</span>
                </Link>
              ))}
            </div>
          </div>
        ))}
      </nav>
    </aside>
  );
}
