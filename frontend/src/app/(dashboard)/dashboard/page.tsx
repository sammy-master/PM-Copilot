"use client";

import Link from "next/link";
import {
  FileText,
  BookOpen,
  Map,
  Layers,
  MessageSquare,
  Upload,
  ArrowRight,
  Sparkles,
  Clock,
  FolderOpen,
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/context/AuthContext";

// Quick action cards — each links to a feature
const quickActions = [
  {
    title: "Generate PRD",
    description: "Create a Product Requirements Document from a brief description",
    href: "/dashboard/generate/prd",
    icon: FileText,
    color: "text-blue-400",
    bg: "bg-blue-400/10",
  },
  {
    title: "Write User Stories",
    description: "Generate INVEST-compliant user stories for your features",
    href: "/dashboard/generate/user-stories",
    icon: BookOpen,
    color: "text-violet-400",
    bg: "bg-violet-400/10",
  },
  {
    title: "Build Roadmap",
    description: "Plan your product roadmap with phases and milestones",
    href: "/dashboard/generate/roadmap",
    icon: Map,
    color: "text-emerald-400",
    bg: "bg-emerald-400/10",
  },
  {
    title: "Prioritize Features",
    description: "Score and rank features using RICE, MoSCoW, or ICE",
    href: "/dashboard/prioritize",
    icon: Layers,
    color: "text-amber-400",
    bg: "bg-amber-400/10",
  },
  {
    title: "AI Chat",
    description: "Ask anything about product management and strategy",
    href: "/dashboard/chat",
    icon: MessageSquare,
    color: "text-pink-400",
    bg: "bg-pink-400/10",
  },
  {
    title: "Upload Documents",
    description: "Upload PDFs and ask questions using RAG",
    href: "/dashboard/documents",
    icon: Upload,
    color: "text-cyan-400",
    bg: "bg-cyan-400/10",
  },
];

// Stats shown at the top of the dashboard
const stats = [
  { label: "PRDs Generated", value: "0", icon: FileText },
  { label: "User Stories", value: "0", icon: BookOpen },
  { label: "Documents", value: "0", icon: FolderOpen },
  { label: "AI Chats", value: "0", icon: MessageSquare },
];

export default function DashboardPage() {
  const { user } = useAuth();

  // Get greeting based on time of day
  const hour = new Date().getHours();
  const greeting =
    hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : "Good evening";

  return (
    <div className="space-y-8 max-w-5xl">

      {/* Welcome Banner */}
      <div className="rounded-xl border border-border bg-gradient-to-r from-primary/5 via-primary/3 to-transparent p-6">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-2 text-primary mb-1">
              <Sparkles size={16} />
              <span className="text-xs font-medium uppercase tracking-wider">
                AI-Powered
              </span>
            </div>
            <h2 className="text-2xl font-bold text-foreground">
              {greeting}, {user?.name?.split(" ")[0]} 👋
            </h2>
            <p className="text-muted-foreground mt-1 text-sm">
              What would you like to build today?
            </p>
          </div>
          <Button asChild size="sm" className="hidden sm:flex">
            <Link href="/dashboard/chat">
              <MessageSquare size={14} />
              Start Chatting
            </Link>
          </Button>
        </div>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <Card key={stat.label} className="border-border/50">
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <Icon size={16} className="text-muted-foreground" />
                  <div>
                    <p className="text-2xl font-bold">{stat.value}</p>
                    <p className="text-[11px] text-muted-foreground">{stat.label}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Quick Actions Grid */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-foreground">Quick Actions</h3>
          <Link
            href="/dashboard/history"
            className="flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground transition-colors"
          >
            <Clock size={12} />
            View History
          </Link>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {quickActions.map((action) => {
            const Icon = action.icon;
            return (
              <Link key={action.href} href={action.href}>
                <Card className="border-border/50 hover:border-border hover:bg-accent/30 transition-all duration-200 cursor-pointer group h-full">
                  <CardContent className="p-5">
                    <div className="flex items-start gap-4">
                      <div className={`p-2.5 rounded-lg ${action.bg} flex-shrink-0`}>
                        <Icon size={18} className={action.color} />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center justify-between">
                          <h4 className="text-sm font-medium text-foreground">
                            {action.title}
                          </h4>
                          <ArrowRight
                            size={14}
                            className="text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0"
                          />
                        </div>
                        <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
                          {action.description}
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </Link>
            );
          })}
        </div>
      </div>

      {/* About This Project */}
      <Card className="border-border/50 border-dashed">
        <CardContent className="p-5">
          <p className="text-xs text-muted-foreground text-center">
            <span className="font-medium text-foreground">PM Copilot</span> — B.Tech Final Year Project ·
            Built with Next.js, FastAPI, LangChain, Ollama & ChromaDB
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
