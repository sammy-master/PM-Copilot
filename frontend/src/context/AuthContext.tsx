"use client";

/**
 * PM Copilot - Auth Context
 * --------------------------
 * Global state for authentication.
 * 
 * WHY CONTEXT?
 *   Every page needs to know if the user is logged in.
 *   Instead of passing user data through props on every component,
 *   we use React Context — any component can access the user anywhere.
 * 
 * HOW JWT WORKS HERE:
 *   1. User logs in → backend returns JWT token
 *   2. We store token in localStorage (persists across refresh)
 *   3. Every API request includes token in Authorization header
 *   4. On app load, we check localStorage → fetch user profile → set state
 */

import {
  createContext,
  useContext,
  useEffect,
  useState,
  useCallback,
  ReactNode,
} from "react";
import { useRouter } from "next/navigation";
import { api, setAuthToken, clearAuthToken } from "@/lib/api";
import type { User } from "@/types";

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (token: string, user: User) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true); // true while checking localStorage
  const router = useRouter();

  // On app mount: restore session from localStorage
  useEffect(() => {
    const savedToken = localStorage.getItem("pm_copilot_token");

    if (savedToken) {
      setAuthToken(savedToken);
      setToken(savedToken);

      // Verify token is still valid by fetching the user profile
      api
        .get("/auth/me")
        .then((res) => {
          setUser(res.data);
        })
        .catch(() => {
          // Token is expired or invalid — clear it
          localStorage.removeItem("pm_copilot_token");
          clearAuthToken();
          setToken(null);
        })
        .finally(() => {
          setIsLoading(false);
        });
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = useCallback((newToken: string, userData: User) => {
    // Save token to localStorage so it survives page refresh
    localStorage.setItem("pm_copilot_token", newToken);
    setAuthToken(newToken); // Set on axios default headers
    setToken(newToken);
    setUser(userData);
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem("pm_copilot_token");
    clearAuthToken();
    setToken(null);
    setUser(null);
    router.push("/sign-in");
  }, [router]);

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isLoading,
        isAuthenticated: !!user,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook for easy access
export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside <AuthProvider>");
  }
  return context;
}
