import requests
import hmac
from typing import Any, Optional

# Global dictionary mapping user IDs to their trusted signatures.
TRUSTED_USER_PROFILES: dict[str, str] = {
    # Example entries (replace with real data)
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "user456": "1a2b3c4d5e6f7g8h9i0j",
}

# Base URL for the remote user profile service.
BASE_URL = "https://api.example.com/users"


def retrieve_user_info(uid: str, sig: str) -> Optional[Any]:
    """
    Fetch a user profile from the remote system and verify its signature.

    Parameters
    ----------
    uid : str
        Unique identifier of the user.
    sig : str
        Cryptographic signature accompanying the profile data.

    Returns
    -------
    dict | None
        The user profile as a dictionary if the signature is valid,
        otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to a connectivity issue.
    """
    # Ensure we have a trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if not expected_sig:
        # Unknown user: treat as untrusted
        return None

    # Verify the provided signature against the trusted one using constant‑time comparison
    if not hmac.compare_digest(sig, expected_sig):
        return None

    # Build the request URL
    url = f"{BASE_URL}/{uid}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.ConnectionError,
            requests.Timeout,
            requests.HTTPError) as exc:
        # Wrap any network/HTTP error in a ConnectionError for the caller
        raise ConnectionError(f"Failed to retrieve profile for user {uid}") from exc

    try:
        # Assume the remote service returns JSON
        profile_data = response.json()
    except ValueError as exc:
        # Invalid JSON payload; treat as a connectivity problem
        raise ConnectionError(f"Invalid response format for user {uid}") from exc

    return profile_data