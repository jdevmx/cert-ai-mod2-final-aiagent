/**
 * Unit tests for UserProfilePanel — renders rig specs for each seed profile.
 */

import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { UserProfilePanel } from "../components/UserProfilePanel";
import type { UserProfile } from "../types";

const TRAIL_PRO: UserProfile = {
  user_id: "user_trail_pro",
  display_name: "Marcus B.",
  email: "marcus@example.com",
  vehicle: "2021 Ford Bronco Wildtrak",
  lift_height_in: 4.0,
  tire_size: "35x12.50R17",
  locking_diffs: true,
  primary_use: "trail",
  skill_level: "expert",
};

const OVERLANDER: UserProfile = {
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

const WEEKEND_WARRIOR: UserProfile = {
  user_id: "user_weekend_warrior",
  display_name: "Derek T.",
  email: "derek@example.com",
  vehicle: "2020 Jeep Wrangler JL Sport",
  lift_height_in: 0,
  tire_size: "265/70R17",
  locking_diffs: false,
  primary_use: "trail",
  skill_level: "beginner",
};

describe("UserProfilePanel", () => {
  it("renders the trail pro profile correctly", () => {
    render(<UserProfilePanel profile={TRAIL_PRO} />);
    expect(screen.getByText("Marcus B.")).toBeInTheDocument();
    expect(screen.getByText("2021 Ford Bronco Wildtrak")).toBeInTheDocument();
    expect(screen.getByText('4" suspension lift')).toBeInTheDocument();
    expect(screen.getByText("35x12.50R17")).toBeInTheDocument();
    expect(screen.getByText("Yes")).toBeInTheDocument();
    expect(screen.getByText("expert")).toBeInTheDocument();
  });

  it("renders the overlander profile correctly", () => {
    render(<UserProfilePanel profile={OVERLANDER} />);
    expect(screen.getByText("Sofia R.")).toBeInTheDocument();
    expect(screen.getByText("2022 Toyota 4Runner TRD Pro")).toBeInTheDocument();
    expect(screen.getByText("overlanding")).toBeInTheDocument();
  });

  it("shows 'Stock (no lift)' when lift_height_in is 0", () => {
    render(<UserProfilePanel profile={WEEKEND_WARRIOR} />);
    expect(screen.getByText("Stock (no lift)")).toBeInTheDocument();
  });

  it("shows 'No' for locking diffs when false", () => {
    render(<UserProfilePanel profile={WEEKEND_WARRIOR} />);
    expect(screen.getByText("No")).toBeInTheDocument();
  });

  it("displays beginner skill level", () => {
    render(<UserProfilePanel profile={WEEKEND_WARRIOR} />);
    expect(screen.getByText("beginner")).toBeInTheDocument();
  });

  it("displays the user email", () => {
    render(<UserProfilePanel profile={OVERLANDER} />);
    expect(screen.getByText("sofia@example.com")).toBeInTheDocument();
  });
});
