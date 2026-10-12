import hmac
import json
from typing import Any, Dict, Optional

import requests  # pip install requests if not already available

# Global mapping of user IDs to their expected cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (in a real system these would be populated from a secure source)
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "alice":   "deadbeefcafebabe1234",
}

def _fetch_remote_profile(uid: str) -> Dict[str, Any]:
    """
    Fetches the user profile from a remote service.

    Args:
        uid: The unique identifier for the user.

    Returns:
        A dictionary representing the user's profile data.

    Raises:
        ConnectionError: If the remote service cannot be reached or returns an error status.
    """
    url = f"https://api.example.com/users/{uid}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        raise ConnectionError(f"Failed to fetch profile for UID '{uid}': {exc}") from exc

    try:
        return response.json()
    except json.JSONDecodeError as exc:
        raise ConnectionError(f"Invalid JSON returned for UID '{uid}': {exc}") from exc

def retrieve_user_profile(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves a user profile from a remote service and validates its cryptographic signature.

    Args:
        uid: The unique identifier for the user whose profile is being fetched.
        sig: The cryptographic signature associated with the user profile.

    Returns:
        The user profile dictionary if the provided signature matches the expected one;
        otherwise, None.

    Raises:
        ConnectionError: If it's not possible to fetch the profile from the remote service.
    """
    # 1. Verify that we have a known expected signature for this UID
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if expected_sig is None:
        # Unknown user – treat as untrusted
        return None

    # 2. Perform a constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(sig, expected_sig):
        # Signature mismatch – do not trust the data
        return None

    # 3. Fetch the profile from the remote service
    profile = _fetch_remote_profile(uid)

    # 4. Return the trusted profile data
    return profile