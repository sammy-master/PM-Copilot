import { redirect } from "next/navigation";

// Root URL "/" always redirects to dashboard.
// Middleware + DashboardLayout handle the auth check.
export default function RootPage() {
  redirect("/dashboard");
}
