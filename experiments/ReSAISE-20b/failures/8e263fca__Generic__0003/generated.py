import hashlib
import json
import random
from typing import Any, Dict, Optional

# Global dictionary mapping user IDs to their expected cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "5d41402abc4b2a76b9719d911017c592",
    "bob":   "7d793037a0760186574b0282f2f435e7",
    # Add more trusted users here
}

# Simulated remote service endpoint (for illustration only)
REMOTE_SERVICE_URL = "https://example.com/api/profile"


def _simulate_remote_fetch(user_id: str) -> Dict[str, Any]:
    """
    Simulate fetching a user profile from a remote service.
    In a real implementation this would be an HTTP request.
    """
    # Randomly simulate network failure
    if random.random() < 0.1:  # 10% chance of failure
        raise ConnectionError(f"Failed to connect to remote service for user {user_id}")

    # Simulated profiles (in reality, you'd parse a JSON response)
    fake_profiles = {
        "alice": {"name": "Alice Smith", "email": "alice@example.com"},
        "bob":   {"name": "Bob Jones",   "email": "bob@example.com"},
    }
    return fake_profiles.get(user_id, {})


def _hash_profile(profile: Dict[str, Any]) -> str:
    """
    Return an MD5 hash of the JSON representation of a profile.
    This is used to compare against the stored signature.
    """
    json_bytes = json.dumps(profile, sort_keys=True).encode("utf-8")
    return hashlib.md5(json_bytes).hexdigest()


def fetch_profile_info(user_ident: str, user_sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from a remote service and validate its signature.

    Parameters
    ----------
    user_ident : str
        The unique identifier for the user whose profile is being fetched.
    user_sig : str
        The cryptographic signature provided for the user profile.

    Returns
    -------
    dict or None
        The user profile dictionary if the signature matches the expected one,
        otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched from the remote service.
    """
    # Validate that the user is trusted
    expected_sig = TRUSTED_USER_PROFILES.get(user_ident)
    if expected_sig is None:
        # Unknown user – no need to fetch
        return None

    # Ensure the provided signature matches the expected one
    if user_sig != expected_sig:
        return None

    # Fetch profile from remote service
    profile = _simulate_remote_fetch(user_ident)

    if not profile:
        # No profile data returned – treat as failure
        raise ConnectionError(f"No profile found for user {user_ident}")

    # Optional: double‑check the signature against the fetched data
    if _hash_profile(profile) != user_sig:
        # Signature mismatch – reject the profile
        return None

    return profile


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    try:
        profile = fetch_profile_info("alice", "5d41402abc4b2a76b9719d911017c592")
        print("Fetched profile:", profile)
    except ConnectionError as exc:
        print("Connection error:", exc)