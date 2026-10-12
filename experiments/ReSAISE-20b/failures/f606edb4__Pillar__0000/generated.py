import json
import hmac
from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException


# Global dictionary mapping user IDs to their correct cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries
    "alice": "a1b2c3d4e5f6g7h8i9j0",
    "bob":   "1234567890abcdef1234",
    # Add more user signatures as needed
}


def retrieve_user_info(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a user profile from the remote system and verify its signature.

    Parameters
    ----------
    uid : str
        Unique identifier of the user.
    sig : str
        Cryptographic signature provided with the profile data.

    Returns
    -------
    dict or None
        The user profile if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to a connectivity issue.
    """
    # URL for fetching user profiles – replace with the actual endpoint.
    url = f"https://api.example.com/users/{uid}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except RequestException as exc:
        # Wrap any requests exception in a ConnectionError to match the spec.
        raise ConnectionError(f"Failed to retrieve user profile for {uid}") from exc

    # Parse JSON response. If parsing fails, treat as an invalid profile.
    try:
        profile_data = response.json()
    except ValueError:
        return None

    # Retrieve the expected signature for this user.
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if expected_sig is None:
        # No trusted signature available; treat as invalid.
        return None

    # Constant‑time comparison to avoid timing attacks (CWE‑693).
    if not hmac.compare_digest(sig, expected_sig):
        return None

    # Signature is valid; return the profile data.
    return profile_data