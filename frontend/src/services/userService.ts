/**
 * User service — wraps the backend /api/users endpoints.
 */

import type { ConversationHistory, UserProfile } from "../types";

const API_BASE = import.meta.env.VITE_API_URL ?? "";

export type UserService = {
  getUserProfile: (userId: string) => Promise<UserProfile>;
  getConversationHistory: (userId: string) => Promise<ConversationHistory>;
  clearConversation: (userId: string) => Promise<void>;
};

export async function getUserProfile(userId: string): Promise<UserProfile> {
  const res = await fetch(`${API_BASE}/api/users/${encodeURIComponent(userId)}/profile`);
  if (!res.ok) {
    console.error("Profile fetch failed:", res.status);
    throw new Error(`Profile fetch error: ${res.status}`);
  }
  return res.json() as Promise<UserProfile>;
}

export async function getConversationHistory(
  userId: string,
): Promise<ConversationHistory> {
  const res = await fetch(
    `${API_BASE}/api/users/${encodeURIComponent(userId)}/conversations`,
  );
  if (!res.ok) {
    console.error("Conversation fetch failed:", res.status);
    throw new Error(`Conversation fetch error: ${res.status}`);
  }
  return res.json() as Promise<ConversationHistory>;
}

export async function clearConversation(userId: string): Promise<void> {
  const res = await fetch(
    `${API_BASE}/api/users/${encodeURIComponent(userId)}/conversations`,
    { method: "DELETE" },
  );
  if (!res.ok && res.status !== 204) {
    console.error("Conversation clear failed:", res.status);
    throw new Error(`Conversation clear error: ${res.status}`);
  }
}

/** Default injectable service object used in production. */
export const userService: UserService = {
  getUserProfile,
  getConversationHistory,
  clearConversation,
};
