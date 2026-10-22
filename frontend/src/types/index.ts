/**
 * Global TypeScript type definitions for PM Copilot.
 * Import from "@/types" anywhere in the frontend.
 */

// ---- User & Auth ----
export interface User {
  id: string;
  email: string;
  name: string;
  createdAt: string;
}

// ---- Projects ----
export interface Project {
  id: string;
  userId: string;
  name: string;
  description: string;
  createdAt: string;
}

// ---- Documents (RAG) ----
export interface Document {
  id: string;
  projectId: string;
  fileName: string;
  fileType: "pdf" | "docx";
  chunkCount: number;
  createdAt: string;
}

// ---- Chat ----
export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  createdAt: string;
}

export interface ChatSession {
  id: string;
  projectId: string;
  title: string;
  messages: ChatMessage[];
  createdAt: string;
}

// ---- Generated Artifacts ----
export type ArtifactType = "prd" | "user_story" | "roadmap" | "prioritization";

export interface HistoryItem {
  id: string;
  projectId: string;
  type: ArtifactType;
  title: string;
  outputContent: string;
  createdAt: string;
}

// ---- Generation Form Inputs ----
export interface PrdInput {
  featureName: string;
  description: string;
  targetAudience: string;
  goals: string;
  projectId: string;
}

export interface UserStoryInput {
  featureName: string;
  userType: string;
  context: string;
  projectId: string;
  count: number;
}

export interface RoadmapInput {
  productName: string;
  currentState: string;
  goals: string;
  timeframe: string;
  projectId: string;
}

export interface PrioritizationInput {
  features: string;
  framework: "moscow" | "rice" | "ice";
  context: string;
  projectId: string;
}

// ---- RAG Query ----
export interface RagQueryResult {
  answer: string;
  sources: Array<{
    chunkId: string;
    text: string;
    source: string;
  }>;
}

// ---- API Response ----
export interface ApiResponse<T> {
  data: T;
  message?: string;
}
