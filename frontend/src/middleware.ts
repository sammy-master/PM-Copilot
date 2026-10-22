/**
 * Next.js Middleware — Route Protection
 * ----------------------------------------
 * Runs on every request BEFORE the page loads.
 * 
 * Rules:
 *   - If visiting /dashboard/* without a token → redirect to /sign-in
 *   - If visiting /sign-in or /sign-up with a token → redirect to /dashboard
 * 
 * NOTE: Middleware can only read cookies, not localStorage.
 * So we store the token in BOTH localStorage (for API calls)
 * and a cookie (for middleware to read).
 */

import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const PUBLIC_ROUTES = ["/sign-in", "/sign-up"];
const PROTECTED_PREFIX = "/dashboard";

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const token = request.cookies.get("pm_copilot_token")?.value;

  const isPublicRoute = PUBLIC_ROUTES.some((route) =>
    pathname.startsWith(route)
  );
  const isProtectedRoute = pathname.startsWith(PROTECTED_PREFIX);

  // Redirect unauthenticated users away from protected pages
  if (isProtectedRoute && !token) {
    return NextResponse.redirect(new URL("/sign-in", request.url));
  }

  // Redirect authenticated users away from login/register pages
  if (isPublicRoute && token) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/dashboard/:path*",
    "/sign-in",
    "/sign-up",
  ],
};
