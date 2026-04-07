/** Shared TypeScript types for the 4x4 Off-Road Advisor. */

export type PrimaryUse = "trail" | "overlanding" | "daily";
export type SkillLevel = "beginner" | "intermediate" | "expert";

export type UserProfile = {
  user_id: string;
  display_name: string;
  email: string;
  vehicle: string;
  lift_height_in: number;
  tire_size: string;
  locking_diffs: boolean;
  primary_use: PrimaryUse;
  skill_level: SkillLevel;
  created_at?: string;
  updated_at?: string;
};

export type MessageRole = "human" | "ai";

export type Message = {
  role: MessageRole;
  content: string;
  /** True while the AI token stream for this message is still open. */
  isStreaming?: boolean;
  timestamp?: string;
};

export type ConversationHistory = {
  user_id: string;
  messages: Message[];
  updated_at?: string;
};

export type ChatResponse = {
  user_id: string;
  message: string;
  conversation_length: number;
};

/** The 3 seed users available in the user selector. */
export type SeedUser = {
  user_id: string;
  label: string;
  description: string;
};

export const SEED_USERS: SeedUser[] = [
  {
    user_id: "user_trail_pro",
    label: "Marcus B. — Trail Pro",
    description: "2021 Ford Bronco Wildtrak · 4\" lift · 35s · Expert",
  },
  {
    user_id: "user_overlander",
    label: "Sofia R. — Overlander",
    description: "2022 Toyota 4Runner TRD Pro · 3\" lift · 285s · Intermediate",
  },
  {
    user_id: "user_weekend_warrior",
    label: "Derek T. — Weekend Warrior",
    description: "2020 Jeep Wrangler JL Sport · 2\" lift · Beginner",
  },
];
