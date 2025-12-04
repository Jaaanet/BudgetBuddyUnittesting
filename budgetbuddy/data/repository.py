import json
from pathlib import Path
from budgetbuddy.core.models import UserProfile

DATA_FILE = Path("budgetbuddy_data.json")


def load_profiles():
    """Load all profiles from the JSON file. Return a dict name -> UserProfile."""
    if not DATA_FILE.exists():
        return {}

    with DATA_FILE.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    profiles = {}
    for name, pdata in raw.items():
        profiles[name] = UserProfile.from_dict(pdata)
    return profiles


def save_profiles(profiles):
    """Save the profiles dict to the JSON file."""
    raw = {}
    for name, profile in profiles.items():
        raw[name] = profile.to_dict()

    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(raw, f, indent=2)


def create_profile(profiles, name):
    """Create a new profile and add it to the profiles dict."""
    profile = UserProfile(name)
    profiles[name] = profile
    return profile


def delete_profile(profiles, name):
    """Delete a profile by name, if it exists."""
    if name in profiles:
        del profiles[name]


def rename_profile(profiles, old, new):
    """Rename a profile in the profiles dict."""
    if old not in profiles:
        return
    profile = profiles[old]
    del profiles[old]
    profile.name = new
    profiles[new] = profile
