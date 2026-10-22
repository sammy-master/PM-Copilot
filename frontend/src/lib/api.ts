/**
 * PM Copilot — Axios API Client
 * --------------------------------
 * Single Axios instance used by the entire frontend.
 * baseURL points to the FastAPI backend.
 *
 * setAuthToken()  — called after login to attach JWT to every request
 * clearAuthToken() — called after logout
 */

import axios from "axios";

const BACKEND_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const api = axios.create({
  baseURL: BACKEND_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

/** Attach the JWT token to all future requests. */
export function setAuthToken(token: string) {
  api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
}

/** Remove the JWT token (on logout). */
export function clearAuthToken() {
  delete api.defaults.headers.common["Authorization"];
}
