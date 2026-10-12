import json
import hmac
import requests
from typing import Any, Dict

# Global dictionary mapping user IDs to their trusted signature (hex string)
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries; in production these would be populated from a secure source
    "user123": "a3f5c8e9d0b1f2a4c6d7e8f90123456789abcdef0123456789abcdef0123456",
    "user456": "b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f901234",
    # ...
}

def _fetch_remote_profile(user_id: str) -> Dict[str, Any]:
    """
    Internal helper to fetch profile data from the remote service.
    Raises requests.ConnectionError if the request fails.
    """
    url = f"https://api.example.com/users/{user_id}/profile"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        # Propagate a ConnectionError to match the required exception type
        raise ConnectionError(f"Failed to fetch profile for {user_id}") from exc

    # Assume the remote service returns JSON
    return response.json()

def fetch_user_profile(user_id: str, signature: str) -> Any | None:
    """
    Retrieve a user profile from the remote service and verify its signature.

    Parameters
    ----------
    user_id : str
        Unique identifier of the user.
    signature : str
        Hex-encoded cryptographic signature accompanying the profile data.

    Returns
    -------
    Any | None
        The user profile data if the signature is valid; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the profile could not be fetched from the remote service.
    """
    # Fetch the profile data
    profile_data = _fetch_remote_profile(user_id)

    # Retrieve the trusted signature for this user
    trusted_sig = TRUSTED_USER_PROFILES.get(user_id)
    if not trusted_sig:
        # No trusted signature known for this user
        return None

    # Ensure the signatures are compared in a timing‑safe manner
    if not hmac.compare_digest(signature.lower(), trusted_sig.lower()):
        # Signature mismatch; do not trust the data
        return None

    # All checks passed – return the profile data
    return profile_data