/**
 * Unit tests for the useSSEChat hook.
 *
 * All tests use StubEventSource — no real EventSource, no network, instant.
 */

import { act, renderHook } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { useSSEChat } from "../hooks/useSSEChat";
import { makeStubChatService } from "./stubs/stubChatService";

describe("useSSEChat", () => {
  it("starts with an empty message list", () => {
    const svc = makeStubChatService();
    const { result } = renderHook(() => useSSEChat("u1", svc));
    expect(result.current.messages).toEqual([]);
    expect(result.current.isStreaming).toBe(false);
  });

  it("appends the human message immediately on sendMessage", () => {
    const svc = makeStubChatService();
    const { result } = renderHook(() => useSSEChat("u1", svc));

    act(() => {
      result.current.sendMessage("What tire pressure for sand?");
    });

    expect(result.current.messages[0]).toMatchObject({
      role: "human",
      content: "What tire pressure for sand?",
    });
  });

  it("sets isStreaming to true after sendMessage", () => {
    const svc = makeStubChatService();
    const { result } = renderHook(() => useSSEChat("u1", svc));

    act(() => {
      result.current.sendMessage("Hello");
    });

    expect(result.current.isStreaming).toBe(true);
  });

  it("accumulates tokens from SSE message events", () => {
    const svc = makeStubChatService();
    const { result } = renderHook(() => useSSEChat("u1", svc));

    act(() => {
      result.current.sendMessage("tire pressure?");
    });

    act(() => {
      svc._lastSource!.emit("message", "Air");
    });
    act(() => {
      svc._lastSource!.emit("message", " down");
    });
    act(() => {
      svc._lastSource!.emit("message", " to 15 PSI.");
    });

    const aiMsg = result.current.messages.find((m) => m.role === "ai");
    expect(aiMsg?.content).toBe("Air down to 15 PSI.");
    expect(aiMsg?.isStreaming).toBe(true);
  });

  it("marks isStreaming false on done event", () => {
    const svc = makeStubChatService();
    const { result } = renderHook(() => useSSEChat("u1", svc));

    act(() => {
      result.current.sendMessage("Hello");
    });
    act(() => {
      svc._lastSource!.emit("message", "Response text");
    });
    act(() => {
      svc._lastSource!.emit("done", "{}");
    });

    expect(result.current.isStreaming).toBe(false);
    const aiMsg = result.current.messages.find((m) => m.role === "ai");
    expect(aiMsg?.isStreaming).toBe(false);
  });

  it("sets error state and removes streaming bubble on error event", () => {
    const svc = makeStubChatService();
    const { result } = renderHook(() => useSSEChat("u1", svc));

    act(() => {
      result.current.sendMessage("Hello");
    });
    act(() => {
      svc._lastSource!.emit("error", JSON.stringify({ detail: "Agent failure" }));
    });

    expect(result.current.error).toBe("Agent failure");
    expect(result.current.isStreaming).toBe(false);
    expect(result.current.messages.find((m) => m.isStreaming)).toBeUndefined();
  });

  it("loadMessages replaces the message list", () => {
    const svc = makeStubChatService();
    const { result } = renderHook(() => useSSEChat("u1", svc));

    act(() => {
      result.current.loadMessages([
        { role: "human", content: "Loaded message" },
        { role: "ai", content: "Loaded response" },
      ]);
    });

    expect(result.current.messages).toHaveLength(2);
    expect(result.current.messages[0].content).toBe("Loaded message");
  });

  it("does not start a new stream if already streaming", () => {
    const svc = makeStubChatService();
    const { result } = renderHook(() => useSSEChat("u1", svc));

    act(() => {
      result.current.sendMessage("First message");
    });
    const firstSource = svc._lastSource;

    act(() => {
      result.current.sendMessage("Second message (should be ignored)");
    });

    // The source should not have changed (second call was a no-op)
    expect(svc._lastSource).toBe(firstSource);
  });
});
