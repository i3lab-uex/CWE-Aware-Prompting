import json
import hmac
import hashlib
from typing import Any, Dict, Optional

# Simulated trusted signature mapping (user_id -> expected signature)
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "alice":   "e99a18c428cb38d5f260853678922e03",
    # Add more trusted users here
}

# URL of the remote service that returns a JSON profile for a given user ID.
REMOTE_PROFILE_URL = "https://example.com/api/user_profile"


def _fetch_remote_profile(uid: str) -> Dict[str, Any]:
    """
    Fetch the user profile from the remote service.

    Raises:
        ConnectionError: If the HTTP request fails or a non‑200 status is returned.
    """
    import requests  # Local import to keep module lightweight

    try:
        response = requests.get(
            REMOTE_PROFILE_URL,
            params={"uid": uid},
            timeout=5,  # seconds
        )
    except requests.RequestException as exc:
        raise ConnectionError(f"Failed to connect to remote service: {exc}") from exc

    if response.status_code != 200:
        raise ConnectionError(
            f"Remote service returned unexpected status {response.status_code}"
        )

    try:
        return response.json()
    except json.JSONDecodeError as exc:
        raise ConnectionError("Invalid JSON received from remote service") from exc


def retrieve_user_profile(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from a remote service and verify its authenticity.

    Args:
        uid: The unique identifier for the user whose profile is being fetched.
        sig: The cryptographic signature associated with the user profile.

    Returns:
        The user profile dictionary if the signature matches; otherwise, None.

    Raises:
        ConnectionError: If fetching the profile from the remote service fails.
    """
    # Step 1: Verify that we have a trusted signature for this UID
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if expected_sig is None:
        # No trusted signature known for this UID; reject immediately
        return None

    # Step 2: Compare signatures using constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(sig, expected_sig):
        # Signature mismatch – do not fetch the profile
        return None

    # Step 3: Fetch the profile from the remote service
    profile = _fetch_remote_profile(uid)

    # Optional: Additional validation (e.g., check that the profile contains expected fields)
    if not isinstance(profile, dict) or "uid" not in profile:
        # Profile structure is invalid; treat as untrusted
        return None

    # Step 4: Return the verified profile
    return profile


# Example usage (commented out – remove comments to run):
#
# try:
#     profile = retrieve_user_profile("alice", "e99a18c428cb38d5f260853678922e03")
#     if profile:
#         print("Profile retrieved:", profile)
#     else:
#         print("Invalid signature or unknown user.")
# except ConnectionError as e:
#     print(f"Connection error: {e}")