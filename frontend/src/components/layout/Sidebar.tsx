"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Bot,
  LayoutDashboard,
  MessageSquare,
  FileText,
  BookOpen,
  Map,
  Layers,
  Upload,
  History,
  LogOut,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useAuth } from "@/context/AuthContext";

const navItems = [
  {
    label: "Dashboard",
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    label: "AI Chat",
    href: "/dashboard/chat",
    icon: MessageSquare,
  },
  {
    label: "Generate",
    isSection: true,
  },
  {
    label: "PRD Generator",
    href: "/dashboard/generate/prd",
    icon: FileText,
  },
  {
    label: "User Stories",
    href: "/dashboard/generate/user-stories",
    icon: BookOpen,
  },
  {
    label: "Roadmap",
    href: "/dashboard/generate/roadmap",
    icon: Map,
  },
  {
    label: "Prioritization",
    href: "/dashboard/prioritize",
    icon: Layers,
  },
  {
    label: "Knowledge",
    isSection: true,
  },
  {
    label: "Documents",
    href: "/dashboard/documents",
    icon: Upload,
  },
  {
    label: "History",
    href: "/dashboard/history",
    icon: History,
  },
];

export default function Sidebar() {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  return (
    <aside className="w-60 h-screen bg-card border-r border-border flex flex-col fixed left-0 top-0 z-40">
      {/* Logo */}
      <div className="flex items-center gap-2.5 px-5 py-4 border-b border-border">
        <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-primary/10">
          <Bot className="h-4.5 w-4.5 text-primary" size={18} />
        </div>
        <span className="font-semibold text-sm tracking-tight">PM Copilot</span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto px-3 py-3 space-y-0.5">
        {navItems.map((item, idx) => {
          // Section header
          if (item.isSection) {
            return (
              <p
                key={idx}
                className="px-2 pt-4 pb-1 text-[10px] uppercase tracking-widest text-muted-foreground/60 font-medium"
              >
                {item.label}
              </p>
            );
          }

          const isActive = pathname === item.href;
          const Icon = item.icon!;

          return (
            <Link
              key={item.href}
              href={item.href!}
              className={cn(
                "flex items-center gap-2.5 px-2.5 py-2 rounded-md text-sm transition-colors",
                isActive
                  ? "bg-primary/10 text-primary font-medium"
                  : "text-muted-foreground hover:bg-accent hover:text-foreground"
              )}
            >
              <Icon size={16} className="flex-shrink-0" />
              {item.label}
            </Link>
          );
        })}
      </nav>

      {/* User Profile + Logout */}
      <div className="border-t border-border p-3">
        <div className="flex items-center gap-2.5 px-2 py-2 rounded-md">
          {/* Avatar */}
          <div className="w-7 h-7 rounded-full bg-primary/20 flex items-center justify-center text-xs font-semibold text-primary flex-shrink-0">
            {user?.name?.charAt(0).toUpperCase() || "U"}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs font-medium truncate">{user?.name}</p>
            <p className="text-[10px] text-muted-foreground truncate">{user?.email}</p>
          </div>
          <button
            onClick={logout}
            className="text-muted-foreground hover:text-foreground transition-colors flex-shrink-0"
            title="Sign out"
          >
            <LogOut size={14} />
          </button>
        </div>
      </div>
    </aside>
  );
}
