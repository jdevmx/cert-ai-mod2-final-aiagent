/**
 * useSSEChat — manages the EventSource lifecycle and message state for
 * real-time streaming chat.
 *
 * The `service` parameter defaults to the real chatService but can be
 * replaced with a stub in tests (Nullable Infrastructure pattern).
 */

import { useEffect, useRef, useState } from "react";
import { chatService } from "../services/chatService";
import type { ChatService } from "../services/chatService";
import type { Message } from "../types";

const STREAMING_PLACEHOLDER_ID = "__streaming__";

export function useSSEChat(userId: string, service: ChatService = chatService) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const esRef = useRef<EventSource | null>(null);

  // Close any open EventSource on unmount
  useEffect(() => {
    return () => {
      esRef.current?.close();
    };
  }, []);

  /** Replace the current message list (used when loading history). */
  const loadMessages = (loaded: Message[]) => {
    setMessages(loaded);
  };

  const sendMessage = (text: string) => {
    if (isStreaming) return;

    // Close any lingering stream
    esRef.current?.close();
    setError(null);

    // Append the human message immediately
    setMessages((prev) => [...prev, { role: "human", content: text }]);

    // Add a streaming placeholder for the AI response
    setMessages((prev) => [
      ...prev,
      { role: "ai", content: "", isStreaming: true },
    ]);
    setIsStreaming(true);

    const es = service.startSSEStream(userId, text);
    esRef.current = es;

    // Accumulate tokens into the last (streaming) message
    es.addEventListener("message", (event: MessageEvent<string>) => {
      const token = event.data as string;
      setMessages((prev) => {
        const updated = [...prev];
        const last = updated[updated.length - 1];
        if (last?.isStreaming) {
          updated[updated.length - 1] = {
            ...last,
            content: last.content + token,
          };
        }
        return updated;
      });
    });

    es.addEventListener("done", () => {
      // Finalise the streaming message
      setMessages((prev) => {
        const updated = [...prev];
        const last = updated[updated.length - 1];
        if (last?.isStreaming) {
          updated[updated.length - 1] = { ...last, isStreaming: false };
        }
        return updated;
      });
      setIsStreaming(false);
      es.close();
      esRef.current = null;
    });

    es.addEventListener("error", (event: MessageEvent<string>) => {
      let detail = "Streaming error";
      try {
        const parsed = JSON.parse(event.data ?? "{}") as { detail?: string };
        detail = parsed.detail ?? detail;
      } catch {
        // keep default message
      }
      setError(detail);
      setIsStreaming(false);
      // Remove the empty streaming placeholder
      setMessages((prev) => prev.filter((m) => !m.isStreaming));
      es.close();
      esRef.current = null;
    });

    // Handle low-level EventSource connection errors
    es.onerror = () => {
      if (es.readyState === EventSource.CLOSED) {
        setIsStreaming(false);
        setMessages((prev) => prev.filter((m) => !m.isStreaming));
        esRef.current = null;
      }
    };
  };

  return { messages, isStreaming, error, sendMessage, loadMessages };
}
