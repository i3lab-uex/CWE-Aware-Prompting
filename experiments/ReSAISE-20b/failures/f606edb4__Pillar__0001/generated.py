import json
from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException

# Global dictionary mapping user IDs to their trusted signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries; populate with real data as needed.
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "user456": "abcdef1234567890",
}

# Endpoint that returns the user profile data.
USER_PROFILE_ENDPOINT = "https://api.example.com/user/profile"


def _constant_time_compare(val1: str, val2: str) -> bool:
    """
    Perform a constant‑time comparison of two strings to mitigate timing attacks.
    """
    if len(val1) != len(val2):
        return False
    result = 0
    for x, y in zip(val1.encode(), val2.encode()):
        result |= x ^ y
    return result == 0


def retrieve_user_info(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a user profile from the remote system and verify its cryptographic signature.

    Parameters
    ----------
    uid : str
        The unique identifier of the user.
    sig : str
        The cryptographic signature supplied with the profile data.

    Returns
    -------
    dict | None
        The user profile data if the signature is valid; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to a connectivity issue.
    """
    # Verify that the provided signature matches the trusted one.
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if expected_sig is None:
        # Unknown user; no trusted signature available.
        return None

    if not _constant_time_compare(sig, expected_sig):
        # Signature does not match; reject the data.
        return None

    # At this point we trust the signature, so proceed to fetch the data.
    try:
        response = requests.get(
            USER_PROFILE_ENDPOINT,
            params={"uid": uid},
            timeout=5.0,  # seconds
        )
        response.raise_for_status()
    except RequestException as exc:
        # Convert any request‑related exception into a ConnectionError.
        raise ConnectionError(f"Failed to fetch user profile for {uid}") from exc

    try:
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        # The remote service returned non‑JSON data; treat it as a connectivity issue.
        raise ConnectionError(f"Invalid JSON response for user {uid}") from exc

    return profile_data