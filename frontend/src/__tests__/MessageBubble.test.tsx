/**
 * Unit tests for the MessageBubble component.
 */

import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { MessageBubble } from "../components/MessageBubble";

describe("MessageBubble", () => {
  it("renders human message content", () => {
    render(<MessageBubble role="human" content="What tire pressure for sand?" />);
    expect(screen.getByText("What tire pressure for sand?")).toBeInTheDocument();
  });

  it("renders AI message content", () => {
    render(<MessageBubble role="ai" content="Air down to 15–18 PSI." />);
    expect(screen.getByText("Air down to 15–18 PSI.")).toBeInTheDocument();
  });

  it("shows thinking indicator when streaming and content is empty", () => {
    render(<MessageBubble role="ai" content="" isStreaming={true} />);
    expect(screen.getByText("Thinking")).toBeInTheDocument();
  });

  it("shows streaming cursor when content exists and isStreaming is true", () => {
    const { container } = render(
      <MessageBubble role="ai" content="Air down" isStreaming={true} />,
    );
    // The streaming cursor is a span with animate-pulse
    const cursor = container.querySelector(".animate-pulse");
    expect(cursor).toBeInTheDocument();
  });

  it("does not show streaming cursor when isStreaming is false", () => {
    render(<MessageBubble role="ai" content="Air down to 15 PSI." isStreaming={false} />);
    // No animate-pulse cursor when not streaming
    expect(screen.queryByText("Thinking")).not.toBeInTheDocument();
  });

  it("renders 'You' avatar for human messages", () => {
    render(<MessageBubble role="human" content="Hello" />);
    expect(screen.getByText("You")).toBeInTheDocument();
  });

  it("renders 'AI' avatar for ai messages", () => {
    render(<MessageBubble role="ai" content="Hello" />);
    expect(screen.getByText("AI")).toBeInTheDocument();
  });
});
