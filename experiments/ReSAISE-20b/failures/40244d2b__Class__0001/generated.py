import json
import hmac
from typing import Any, Dict, Optional

import requests  # type: ignore

# Global dictionary mapping user IDs to their expected cryptographic signatures
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user123": "5f2c9b1e7d4a8e6f3c0d1b2a9e5f4c3d",
    "alice":   "7a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d",
    # ... add more entries as needed
}

def _fetch_profile_from_remote(identifier: str) -> Dict[str, Any]:
    """
    Fetch the user profile from a remote system.
    Raises ConnectionError if any network-related issue occurs.
    """
    url = f"https://api.example.com/users/{identifier}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        # Convert all request-related exceptions into a generic ConnectionError
        raise ConnectionError(f"Failed to fetch profile for {identifier}") from exc

    try:
        return response.json()
    except ValueError as exc:  # JSON decoding error
        raise ConnectionError(f"Invalid response format for {identifier}") from exc


def access_user_details(identifier: str, crypt_sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from a remote system and verify its authenticity.

    Parameters:
        identifier (str): Unique user ID.
        crypt_sig  (str): Cryptographic signature accompanying the profile.

    Returns:
        dict: The user profile data if the signature is valid.
        None: If the signature does not match the trusted value.

    Raises:
        ConnectionError: If network connectivity or data retrieval fails.
    """
    # 1. Fetch profile data from the remote system
    profile = _fetch_profile_from_remote(identifier)

    # 2. Retrieve the expected signature from TRUSTED_USER_PROFILES
    expected_sig = TRUSTED_USER_PROFILES.get(identifier)
    if not expected_sig:
        # Unknown user: treat as untrusted
        return None

    # 3. Compare signatures using a timing‑safe comparison to mitigate
    #     timing attacks (CWE-345).
    if not hmac.compare_digest(crypt_sig, expected_sig):
        return None

    # 4. Signature verified – trust the profile data
    return profile