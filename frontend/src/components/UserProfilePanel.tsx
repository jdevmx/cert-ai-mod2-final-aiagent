/** Sidebar panel displaying the active user's rig specifications. */

import type { UserProfile } from "../types";

type UserProfilePanelProps = {
  profile: UserProfile;
};

type SpecRowProps = {
  label: string;
  value: string;
};

function SpecRow({ label, value }: SpecRowProps) {
  return (
    <div className="flex flex-col gap-0.5">
      <span className="text-xs text-gray-500 uppercase tracking-wide">{label}</span>
      <span className="text-sm text-gray-200">{value}</span>
    </div>
  );
}

export function UserProfilePanel({ profile }: UserProfilePanelProps) {
  const liftLabel =
    profile.lift_height_in === 0
      ? "Stock (no lift)"
      : `${profile.lift_height_in}" suspension lift`;

  return (
    <div className="p-4 space-y-5">
      {/* Display name */}
      <div>
        <p className="text-base font-semibold text-white">{profile.display_name}</p>
        <p className="text-xs text-gray-500">{profile.email}</p>
      </div>

      <div className="border-t border-gray-700 pt-4 space-y-4">
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider">
          Rig Specs
        </p>

        <SpecRow label="Vehicle" value={profile.vehicle} />
        <SpecRow label="Lift" value={liftLabel} />
        <SpecRow label="Tires" value={profile.tire_size} />
        <SpecRow
          label="Locking Diffs"
          value={profile.locking_diffs ? "Yes" : "No"}
        />
        <SpecRow label="Primary Use" value={profile.primary_use} />
        <SpecRow label="Skill Level" value={profile.skill_level} />
      </div>
    </div>
  );
}
