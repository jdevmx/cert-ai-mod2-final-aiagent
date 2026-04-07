/** Single chat message bubble for human or AI messages. */

type MessageBubbleProps = {
  role: "human" | "ai";
  content: string;
  isStreaming?: boolean;
};

export function MessageBubble({ role, content, isStreaming = false }: MessageBubbleProps) {
  const isHuman = role === "human";

  return (
    <div className={`flex ${isHuman ? "justify-end" : "justify-start"} mb-3`}>
      {/* Avatar label */}
      {!isHuman && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-xs font-bold mr-2 mt-1">
          AI
        </div>
      )}

      <div
        className={`max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
          isHuman
            ? "bg-blue-600 text-white rounded-br-sm"
            : "bg-gray-700 text-gray-100 rounded-bl-sm"
        }`}
      >
        {/* Show streaming cursor when content is empty and still streaming */}
        {content.length === 0 && isStreaming ? (
          <span className="flex items-center gap-1 text-gray-400 text-xs">
            <span className="animate-pulse">Thinking</span>
            <span className="animate-bounce delay-75">.</span>
            <span className="animate-bounce delay-150">.</span>
            <span className="animate-bounce delay-300">.</span>
          </span>
        ) : (
          <>
            <span className="whitespace-pre-wrap">{content}</span>
            {isStreaming && (
              <span className="inline-block w-1.5 h-4 bg-blue-400 animate-pulse ml-0.5 align-middle" />
            )}
          </>
        )}
      </div>

      {isHuman && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center text-xs font-bold ml-2 mt-1">
          You
        </div>
      )}
    </div>
  );
}
