import json
import hmac
import hashlib
from typing import Any, Dict, Optional

import requests

# Global mapping of trusted user IDs to their expected cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries – replace with real data in production
    "user123": "5f2d1c3e4b6a9f0d8e7c5b1a2f3e4d5c",
    "alice":   "9e8b7a6c5d4f3e2d1c0b9a8f7e6d5c4b",
    # ...
}


def retrieve_user_profile(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from a remote service and verify its signature.

    Parameters
    ----------
    uid : str
        The unique identifier for the user whose profile is being fetched.
    sig : str
        The cryptographic signature associated with the user profile.

    Returns
    -------
    dict | None
        The user profile if the signature matches a trusted one; otherwise None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched from the remote service.
    """
    # 1. Fetch the raw data from the remote endpoint
    try:
        response = requests.get(
            f"https://api.example.com/users/{uid}/profile",
            timeout=5,  # seconds
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Any network/HTTP error is treated as a connection failure
        raise ConnectionError(f"Unable to fetch profile for user {uid}") from exc

    # 2. Parse the JSON payload
    try:
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        raise ConnectionError(f"Invalid JSON received for user {uid}") from exc

    # 3. Verify the signature
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if not expected_sig:
        # Unknown user ID – treat as untrusted
        return None

    # Use hmac.compare_digest to avoid timing attacks (CWE-347 mitigation)
    if not hmac.compare_digest(sig, expected_sig):
        return None

    # 4. Return the verified profile
    return profile_data