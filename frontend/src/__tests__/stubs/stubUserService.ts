/**
 * StubUserService — returns preset profile and conversation data synchronously.
 * No network calls in tests.
 */

import type { ConversationHistory, UserProfile } from "../../types";

export const STUB_PROFILE: UserProfile = {
  user_id: "user_overlander",
  display_name: "Sofia R.",
  email: "sofia@example.com",
  vehicle: "2022 Toyota 4Runner TRD Pro",
  lift_height_in: 3.0,
  tire_size: "285/70R17",
  locking_diffs: true,
  primary_use: "overlanding",
  skill_level: "intermediate",
};

export const STUB_HISTORY: ConversationHistory = {
  user_id: "user_overlander",
  messages: [
    { role: "human", content: "What tire pressure for sand?" },
    { role: "ai", content: "Air down to 15–18 PSI on your 285s." },
  ],
};

export function makeStubUserService(overrides?: {
  profile?: UserProfile;
  history?: ConversationHistory;
  shouldFail?: boolean;
}) {
  const profile = overrides?.profile ?? STUB_PROFILE;
  const history = overrides?.history ?? STUB_HISTORY;
  const shouldFail = overrides?.shouldFail ?? false;

  return {
    getUserProfile: async (_userId: string): Promise<UserProfile> => {
      if (shouldFail) throw new Error("Profile fetch error: 500");
      return profile;
    },
    getConversationHistory: async (_userId: string): Promise<ConversationHistory> => {
      if (shouldFail) throw new Error("Conversation fetch error: 500");
      return history;
    },
    clearConversation: async (_userId: string): Promise<void> => {
      if (shouldFail) throw new Error("Conversation clear error: 500");
    },
  };
}
