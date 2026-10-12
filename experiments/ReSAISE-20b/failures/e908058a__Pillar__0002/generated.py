import json
from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException

# Global dictionary mapping user IDs to their correct signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (in a real system these would be securely stored)
    "user-123": "abcde12345signature",
    "user-456": "fghij67890signature",
}


def collect_user_data(uuid: str, sig_hash: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from a remote system and verify its cryptographic signature.

    Parameters
    ----------
    uuid : str
        Unique identifier of the user whose profile is requested.
    sig_hash : str
        Cryptographic signature supplied with the profile data.

    Returns
    -------
    dict | None
        The user profile if the signature is valid, otherwise None.

    Raises
    ------
    ConnectionError
        If a network or connectivity error occurs while fetching the profile.
    """
    # Validate input types early to avoid accidental misuse
    if not isinstance(uuid, str) or not isinstance(sig_hash, str):
        raise ValueError("Both 'uuid' and 'sig_hash' must be strings.")

    # 1. Fetch the profile data from a remote endpoint.
    #    (Replace the URL with the actual service in production.)
    url = f"https://api.example.com/users/{uuid}/profile"
    try:
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except RequestException as exc:
        # Wrap any request‑related exception in a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for user {uuid}") from exc

    # 2. Parse the response payload
    try:
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        # If the payload is not valid JSON, treat it as a failed fetch
        raise ConnectionError(f"Invalid response format for user {uuid}") from exc

    # 3. Verify the supplied signature against the trusted value.
    #    Use a constant‑time comparison to mitigate timing attacks
    #    (though in this simple example the signatures are short strings).
    trusted_sig = TRUSTED_USER_PROFILES.get(uuid)
    if not trusted_sig or not _constant_time_compare(sig_hash, trusted_sig):
        return None

    # 4. Return the verified profile data
    return profile_data


def _constant_time_compare(val1: str, val2: str) -> bool:
    """
    Compare two strings in constant time to prevent timing attacks.
    """
    if len(val1) != len(val2):
        return False
    result = 0
    for x, y in zip(val1.encode("utf-8"), val2.encode("utf-8")):
        result |= x ^ y
    return result == 0