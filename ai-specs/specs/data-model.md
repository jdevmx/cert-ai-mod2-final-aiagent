# Data Model Documentation

This document describes the Firestore data model for the 4x4 Off-Road Vehicle Advisor AI agent,
including collection names, document schemas, field definitions, and relationships.

## Database

**Firebase Firestore** (NoSQL document store) is used for all persistence. There is no relational
database in this project. The Firebase Admin Python SDK accesses Firestore from the FastAPI backend.

---

## Collections

### 1. `users`

Stores the rig profile for each user. The profile data is injected into the agent's system prompt
on every conversation turn to personalise advice.

**Document ID**: `user_id` (string, application-assigned, e.g. `"user_abc123"`)

**Fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `display_name` | string | yes | User's display name |
| `email` | string | yes | User's email address |
| `vehicle` | string | yes | Vehicle make, model, year (e.g. `"2022 Toyota 4Runner TRD Pro"`) |
| `lift_height_in` | number | yes | Suspension lift height in inches; `0` = stock |
| `tire_size` | string | yes | Tire size string (e.g. `"285/70R17"`) |
| `locking_diffs` | boolean | yes | Whether the rig has factory or aftermarket locking differentials |
| `primary_use` | string (enum) | yes | `"trail"` \| `"overlanding"` \| `"daily"` |
| `skill_level` | string (enum) | yes | `"beginner"` \| `"intermediate"` \| `"expert"` |
| `created_at` | timestamp | yes | Document creation time (server timestamp) |
| `updated_at` | timestamp | yes | Last update time (server timestamp) |

**Validation Rules:**

- `vehicle`, `display_name`, `email` are required and non-empty strings
- `lift_height_in` must be >= 0
- `primary_use` must be one of: `trail`, `overlanding`, `daily`
- `skill_level` must be one of: `beginner`, `intermediate`, `expert`

**Example document:**

```json
{
  "display_name": "Alex T.",
  "email": "alex@example.com",
  "vehicle": "2022 Toyota 4Runner TRD Pro",
  "lift_height_in": 3.0,
  "tire_size": "285/70R17",
  "locking_diffs": true,
  "primary_use": "overlanding",
  "skill_level": "intermediate",
  "created_at": "2026-04-04T10:00:00Z",
  "updated_at": "2026-04-04T10:00:00Z"
}
```

---

### 2. `conversations`

Stores the full chat history for each user as an array of messages. The agent loads this history
before each turn to maintain context across sessions.

**Document ID**: `user_id` (same as the `users` collection — one conversation document per user)

**Fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `user_id` | string | yes | Matches the document ID; denormalized for queries |
| `messages` | array\<Message\> | yes | Ordered array of conversation messages |
| `updated_at` | timestamp | yes | Last message timestamp |

**Message object schema:**

| Field | Type | Description |
|---|---|---|
| `role` | string | `"human"` or `"ai"` |
| `content` | string | Message text |
| `timestamp` | timestamp | When the message was created |

**Example document:**

```json
{
  "user_id": "user_abc123",
  "messages": [
    {
      "role": "human",
      "content": "What tire pressure should I run on sand?",
      "timestamp": "2026-04-04T10:01:00Z"
    },
    {
      "role": "ai",
      "content": "For sand, airing down to 15–18 PSI on your 285/70R17s will dramatically improve flotation. With your 3-inch lift, you have good clearance, so focus on tire volume...",
      "timestamp": "2026-04-04T10:01:05Z"
    }
  ],
  "updated_at": "2026-04-04T10:01:05Z"
}
```

**Notes:**

- Messages are appended via Firestore `ArrayUnion` to avoid read-modify-write races.
- No pagination is implemented in the MVP — all messages are loaded per turn. Consider truncating to the last N messages for very long conversations.
- Clearing a conversation resets `messages` to `[]` and updates `updated_at`.

---

## Access Patterns

| Operation | Collection | Method |
|---|---|---|
| Load user profile for system prompt | `users` | `document(user_id).get()` |
| Create/update user profile | `users` | `document(user_id).set(data, merge=True)` |
| Load conversation history | `conversations` | `document(user_id).get()` |
| Append new messages after agent turn | `conversations` | `document(user_id).update({messages: ArrayUnion([...])})` |
| Clear conversation | `conversations` | `document(user_id).update({messages: [], updated_at: now})` |

---

## Security Rules (Firestore)

For production, apply these Firestore security rules:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Only the backend service account can read/write (no client-side SDK)
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
```

All Firestore access goes through the backend service account (Firebase Admin SDK).
The frontend never accesses Firestore directly.

---

## Design Principles

1. **One document per user**: Both `users` and `conversations` use the `user_id` as the document ID, making all lookups O(1) key-value fetches.
2. **Array-based message storage**: Appending to a Firestore array field is atomic and avoids sub-collection overhead for the conversation size expected in this MVP.
3. **Profile injection**: The `users` document is the source of truth for the system prompt. Any profile update immediately affects the next conversation turn.
4. **No SQL, no migrations**: Firestore's schemaless nature means adding new profile fields (e.g., `winch_brand`) is a backend code change only.
