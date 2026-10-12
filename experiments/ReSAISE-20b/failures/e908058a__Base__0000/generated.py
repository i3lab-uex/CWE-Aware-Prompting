import json
import hmac
from typing import Any, Dict, Optional

import requests

# Global mapping of user IDs to their correct cryptographic signatures
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries – in real usage these would be populated from a secure source
    "user-123": "a1b2c3d4e5f6g7h8i9j0",
    "user-456": "0123456789abcdef1234",
}

# Base URL for the remote user profile service
BASE_PROFILE_URL = "https://api.example.com/user"


def _fetch_profile_from_remote(uuid: str) -> Dict[str, Any]:
    """
    Internal helper that performs the actual HTTP GET request to retrieve
    the user profile JSON. Raises ConnectionError on network failures.
    """
    url = f"{BASE_PROFILE_URL}/{uuid}"
    try:
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Convert any request‑related exception to a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for {uuid}") from exc

    try:
        return response.json()
    except json.JSONDecodeError as exc:
        raise ConnectionError(f"Invalid JSON received for {uuid}") from exc


def collect_user_data(uuid: str, sig_hash: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from a remote system and verify its cryptographic
    signature.

    Parameters:
        uuid (str): The unique identifier for the user.
        sig_hash (str): The cryptographic signature supplied with the profile.

    Returns:
        dict: The user profile data if the signature is valid.
        None: If the signature does not match the trusted value.

    Raises:
        ConnectionError: If there is any connectivity issue or malformed
                         response from the remote system.
    """
    # Fetch profile data from the remote service
    profile = _fetch_profile_from_remote(uuid)

    # Retrieve the trusted signature for this user ID
    expected_sig = TRUSTED_USER_PROFILES.get(uuid)
    if expected_sig is None:
        # No trusted signature known – treat as invalid
        return None

    # Use constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(sig_hash, expected_sig):
        return None

    # Signature verified – return the profile data
    return profile