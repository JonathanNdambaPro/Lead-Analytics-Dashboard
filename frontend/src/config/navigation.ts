import { Home, type LucideIcon } from "lucide-react";

export interface NavigationItem {
  title: string;
  url: string;
  icon: LucideIcon;
}

export const navigationItems: NavigationItem[] = [
  {
    title: "Leads Analytics",
    url: "/",
    icon: Home,
  },
];
