"use client";

import { usePathname } from "next/navigation";
import { Bell } from "lucide-react";
import { useAuth } from "@/context/AuthContext";

// Map route paths to readable page titles
const pageTitles: Record<string, string> = {
  "/dashboard": "Dashboard",
  "/dashboard/chat": "AI Chat",
  "/dashboard/generate/prd": "PRD Generator",
  "/dashboard/generate/user-stories": "User Story Generator",
  "/dashboard/generate/roadmap": "Roadmap Generator",
  "/dashboard/prioritize": "Feature Prioritization",
  "/dashboard/documents": "Documents",
  "/dashboard/history": "History",
};

export default function Header() {
  const pathname = usePathname();
  const { user } = useAuth();

  const title = pageTitles[pathname] || "PM Copilot";

  return (
    <header className="h-14 border-b border-border bg-background/80 backdrop-blur-sm flex items-center justify-between px-6 sticky top-0 z-30">
      {/* Page Title */}
      <h1 className="text-sm font-semibold text-foreground">{title}</h1>

      {/* Right side */}
      <div className="flex items-center gap-3">
        <button className="text-muted-foreground hover:text-foreground transition-colors">
          <Bell size={16} />
        </button>
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-full bg-primary/20 flex items-center justify-center text-xs font-semibold text-primary">
            {user?.name?.charAt(0).toUpperCase() || "U"}
          </div>
          <span className="text-xs font-medium text-foreground hidden sm:block">
            {user?.name}
          </span>
        </div>
      </div>
    </header>
  );
}
