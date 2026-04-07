/** Main chat interface — message list + input bar. */

import { useEffect, useRef } from "react";
import type { Message } from "../types";
import { ChatInput } from "./ChatInput";
import { MessageBubble } from "./MessageBubble";

type ChatWindowProps = {
  messages: Message[];
  isStreaming: boolean;
  streamError: string | null;
  onSend: (message: string) => void;
  disabled?: boolean;
};

export function ChatWindow({
  messages,
  isStreaming,
  streamError,
  onSend,
  disabled = false,
}: ChatWindowProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to the latest message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <section className="flex flex-1 flex-col min-h-0">
      {/* Message list */}
      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-1">
        {messages.length === 0 && !isStreaming && (
          <div className="flex flex-col items-center justify-center h-full text-center text-gray-500 gap-3 py-20">
            <span className="text-5xl">🛞</span>
            <p className="text-lg font-medium text-gray-400">
              Ready to hit the trail?
            </p>
            <p className="text-sm max-w-sm">
              Ask about tire pressure, lift kits, locking diffs, suspension
              upgrades, or trail recommendations — tailored to your rig.
            </p>
          </div>
        )}

        {messages.map((msg, index) => (
          <MessageBubble
            key={index}
            role={msg.role}
            content={msg.content}
            isStreaming={msg.isStreaming}
          />
        ))}

        {/* Stream error */}
        {streamError && (
          <p className="text-center text-sm text-red-400 py-2">{streamError}</p>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input bar */}
      <ChatInput onSend={onSend} disabled={disabled} />
    </section>
  );
}
