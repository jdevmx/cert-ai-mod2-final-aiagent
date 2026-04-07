/**
 * Chat service — wraps the backend /api/chat endpoints.
 *
 * startSSEStream opens a native EventSource to /api/chat/stream.
 * The caller is responsible for attaching event listeners and closing
 * the source when done.
 */

import type { ChatResponse } from "../types";

const API_BASE = import.meta.env.VITE_API_URL ?? "";

export type ChatService = {
  startSSEStream: (userId: string, message: string) => EventSource;
};

export function startSSEStream(userId: string, message: string): EventSource {
  const url =
    `${API_BASE}/api/chat/stream` +
    `?user_id=${encodeURIComponent(userId)}` +
    `&message=${encodeURIComponent(message)}`;
  return new EventSource(url);
}

export async function sendMessage(
  userId: string,
  message: string,
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, message }),
  });
  if (!res.ok) {
    console.error("Chat request failed:", res.status);
    throw new Error(`Chat error: ${res.status}`);
  }
  return res.json() as Promise<ChatResponse>;
}

/** Default injectable service object used in production. */
export const chatService: ChatService = { startSSEStream };
