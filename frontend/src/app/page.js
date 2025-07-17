import Image from "next/image";
import HomeNavbar from "@/components/sidebar";
import { redirect } from "next/dist/server/api-utils";

export default function Home() {
  redirect("/dashboard");
}