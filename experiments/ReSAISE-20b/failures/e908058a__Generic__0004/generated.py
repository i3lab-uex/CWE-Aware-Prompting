import json
from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException

# Global dictionary mapping user IDs to their expected signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries; replace with real data.
    "user-123": "a1b2c3d4e5f6g7h8i9j0",
    "user-456": "z9y8x7w6v5u4t3s2r1q0",
}


def collect_user_data(uuid: str, sig_hash: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from a remote system and verify its cryptographic signature.

    Parameters
    ----------
    uuid : str
        The unique identifier of the user.
    sig_hash : str
        The cryptographic signature accompanying the profile data.

    Returns
    -------
    dict or None
        The parsed JSON profile if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to a network or connectivity issue.
    """
    if not isinstance(uuid, str) or not uuid:
        raise ValueError("uuid must be a non-empty string")
    if not isinstance(sig_hash, str) or not sig_hash:
        raise ValueError("sig_hash must be a non-empty string")

    # Verify the signature against the trusted mapping.
    expected_sig = TRUSTED_USER_PROFILES.get(uuid)
    if expected_sig is None or expected_sig != sig_hash:
        # Signature invalid; do not return data.
        return None

    # Construct the request URL. Replace with actual endpoint as needed.
    url = f"https://api.example.com/users/{uuid}"

    try:
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except RequestException as exc:
        # Any network-related issue is escalated as a ConnectionError.
        raise ConnectionError(f"Failed to fetch profile for user {uuid}") from exc

    try:
        data = response.json()
    except json.JSONDecodeError as exc:
        # Malformed JSON indicates a bad response; treat it as an error.
        raise ConnectionError(f"Invalid JSON received for user {uuid}") from exc

    return data