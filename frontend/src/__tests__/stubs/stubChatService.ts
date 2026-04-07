/**
 * StubEventSource — fires SSE events synchronously in tests.
 * No real EventSource, no network, instant execution.
 */

type Listener = (e: { data: string }) => void;

export class StubEventSource {
  private listeners: Record<string, Listener[]> = {};
  public readyState: number = 1; // OPEN
  static CLOSED = 2;

  addEventListener(type: string, fn: Listener): void {
    (this.listeners[type] ??= []).push(fn);
  }

  /** Synchronously fire all listeners for a given event type. */
  emit(type: string, data: string): void {
    this.listeners[type]?.forEach((fn) => fn({ data }));
  }

  close(): void {
    this.readyState = StubEventSource.CLOSED;
  }

  // Native EventSource also fires onmessage; keep compatible
  set onmessage(_fn: Listener | null) {}
  set onerror(_fn: Listener | null) {}
}

export type StubChatService = {
  startSSEStream: (_userId: string, _msg: string) => StubEventSource;
  _lastSource: StubEventSource | null;
};

export function makeStubChatService(): StubChatService {
  const svc: StubChatService = {
    _lastSource: null,
    startSSEStream: (_userId, _msg) => {
      const src = new StubEventSource();
      svc._lastSource = src;
      return src;
    },
  };
  return svc;
}
