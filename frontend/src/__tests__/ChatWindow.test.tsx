/**
 * Unit tests for the ChatWindow component.
 */

import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { ChatWindow } from "../components/ChatWindow";
import type { Message } from "../types";

const noOp = () => {};

describe("ChatWindow", () => {
  it("shows the empty state when there are no messages", () => {
    render(
      <ChatWindow
        messages={[]}
        isStreaming={false}
        streamError={null}
        onSend={noOp}
      />,
    );
    expect(screen.getByText("Ready to hit the trail?")).toBeInTheDocument();
  });

  it("renders all provided messages", () => {
    const messages: Message[] = [
      { role: "human", content: "What oil for my 4Runner?" },
      { role: "ai", content: "Use 0W-20 full synthetic." },
    ];
    render(
      <ChatWindow
        messages={messages}
        isStreaming={false}
        streamError={null}
        onSend={noOp}
      />,
    );
    expect(screen.getByText("What oil for my 4Runner?")).toBeInTheDocument();
    expect(screen.getByText("Use 0W-20 full synthetic.")).toBeInTheDocument();
  });

  it("displays a stream error message", () => {
    render(
      <ChatWindow
        messages={[]}
        isStreaming={false}
        streamError="Agent failure"
        onSend={noOp}
      />,
    );
    expect(screen.getByText("Agent failure")).toBeInTheDocument();
  });

  it("calls onSend when the user types and presses Enter", async () => {
    const onSend = vi.fn();
    render(
      <ChatWindow
        messages={[]}
        isStreaming={false}
        streamError={null}
        onSend={onSend}
      />,
    );
    const input = screen.getByPlaceholderText(/Ask about your rig/);
    await userEvent.type(input, "Lift kit recommendation{Enter}");
    expect(onSend).toHaveBeenCalledWith("Lift kit recommendation");
  });

  it("disables the input when the disabled prop is true", () => {
    render(
      <ChatWindow
        messages={[]}
        isStreaming={false}
        streamError={null}
        onSend={noOp}
        disabled={true}
      />,
    );
    const input = screen.getByPlaceholderText(/Ask about your rig/);
    expect(input).toBeDisabled();
  });
});
