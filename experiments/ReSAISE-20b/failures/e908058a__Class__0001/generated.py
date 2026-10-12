import json
from typing import Any, Dict, Optional

import requests

# Global mapping of user IDs to their trusted signatures
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (replace with real data)
    "user-123": "sha256:abcdef1234567890",
    "user-456": "sha256:0123456789abcdef",
}

def collect_user_data(uuid: str, sig_hash: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a user profile from a remote system and verify its authenticity.

    Args:
        uuid (str): The unique identifier of the user.
        sig_hash (str): The cryptographic signature accompanying the profile data.

    Returns:
        dict: The user profile if the signature is verified.
        None: If the signature does not match the trusted value.

    Raises:
        ConnectionError: If the profile cannot be retrieved due to a connectivity issue.
    """
    # Build the URL for the remote API (replace with real endpoint)
    url = f"https://api.example.com/users/{uuid}/profile"

    try:
        # Make a secure HTTPS request with SSL verification enabled
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Any network-related issue is treated as a connectivity problem
        raise ConnectionError(f"Failed to fetch profile for {uuid}") from exc

    # Parse the JSON payload
    try:
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        raise ValueError("Response content is not valid JSON") from exc

    # Retrieve the trusted signature for this user
    trusted_sig = TRUSTED_USER_PROFILES.get(uuid)
    if not trusted_sig:
        # No trusted signature available; cannot verify authenticity
        return None

    # Perform a constant‑time comparison to mitigate timing attacks
    if not _constant_time_compare(sig_hash, trusted_sig):
        return None

    return profile_data


def _constant_time_compare(val1: str, val2: str) -> bool:
    """
    Compare two strings in constant time to prevent timing attacks.
    """
    if len(val1) != len(val2):
        return False
    result = 0
    for x, y in zip(val1.encode(), val2.encode()):
        result |= x ^ y
    return result == 0