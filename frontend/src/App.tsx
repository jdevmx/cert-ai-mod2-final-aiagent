/**
 * App — root component.
 *
 * Manages the active user selection (persisted in localStorage) and
 * loads the user profile + conversation history whenever the selection
 * changes.
 */

import { useEffect, useState } from "react";
import { ChatWindow } from "./components/ChatWindow";
import { UserProfilePanel } from "./components/UserProfilePanel";
import { useSSEChat } from "./hooks/useSSEChat";
import { getConversationHistory, getUserProfile } from "./services/userService";
import { SEED_USERS } from "./types";
import type { UserProfile } from "./types";

const STORAGE_KEY = "4x4_advisor_active_user";

function App() {
  const defaultUserId =
    localStorage.getItem(STORAGE_KEY) ??
    (import.meta.env.VITE_DEFAULT_USER_ID as string | undefined) ??
    SEED_USERS[0].user_id;

  const [activeUserId, setActiveUserId] = useState<string>(defaultUserId);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [profileError, setProfileError] = useState<string | null>(null);
  const [loadingProfile, setLoadingProfile] = useState(false);

  const { messages, isStreaming, error, sendMessage, loadMessages } =
    useSSEChat(activeUserId);

  // Persist active user across page refreshes
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, activeUserId);
  }, [activeUserId]);

  // Load profile and conversation history when user changes
  useEffect(() => {
    let cancelled = false;
    setLoadingProfile(true);
    setProfileError(null);
    setProfile(null);

    void (async () => {
      try {
        const [fetchedProfile, history] = await Promise.all([
          getUserProfile(activeUserId),
          getConversationHistory(activeUserId),
        ]);
        if (cancelled) return;
        setProfile(fetchedProfile);
        loadMessages(history.messages);
      } catch (err) {
        if (cancelled) return;
        const message = err instanceof Error ? err.message : "Failed to load profile";
        setProfileError(message);
      } finally {
        if (!cancelled) setLoadingProfile(false);
      }
    })();

    return () => {
      cancelled = true;
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeUserId]);

  const handleUserChange = (userId: string) => {
    setActiveUserId(userId);
  };

  return (
    <div className="flex h-screen bg-gray-900 text-gray-100">
      {/* Sidebar */}
      <aside className="w-72 flex-shrink-0 bg-gray-800 flex flex-col border-r border-gray-700">
        {/* User selector */}
        <div className="p-4 border-b border-gray-700">
          <label
            htmlFor="user-select"
            className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2"
          >
            Active Rider
          </label>
          <select
            id="user-select"
            value={activeUserId}
            onChange={(e) => handleUserChange(e.target.value)}
            className="w-full bg-gray-700 border border-gray-600 rounded-md px-3 py-2 text-sm text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {SEED_USERS.map((u) => (
              <option key={u.user_id} value={u.user_id}>
                {u.label}
              </option>
            ))}
          </select>
          {SEED_USERS.find((u) => u.user_id === activeUserId) && (
            <p className="mt-1 text-xs text-gray-500">
              {SEED_USERS.find((u) => u.user_id === activeUserId)!.description}
            </p>
          )}
        </div>

        {/* Profile panel */}
        <div className="flex-1 overflow-y-auto">
          {loadingProfile && (
            <div className="flex items-center justify-center p-8">
              <div className="animate-spin h-6 w-6 border-2 border-blue-500 border-t-transparent rounded-full" />
            </div>
          )}
          {profileError && (
            <p className="p-4 text-sm text-red-400">{profileError}</p>
          )}
          {profile && !loadingProfile && (
            <UserProfilePanel profile={profile} />
          )}
        </div>
      </aside>

      {/* Main chat area */}
      <main className="flex flex-1 flex-col min-w-0">
        <header className="px-6 py-4 border-b border-gray-700 bg-gray-800">
          <h1 className="text-lg font-bold text-white">4x4 Off-Road Advisor</h1>
          <p className="text-xs text-gray-400">
            Powered by GPT-4o + LangChain · Ask anything about your rig
          </p>
        </header>

        <ChatWindow
          messages={messages}
          isStreaming={isStreaming}
          streamError={error}
          onSend={sendMessage}
          disabled={loadingProfile || isStreaming}
        />
      </main>
    </div>
  );
}

export default App;
