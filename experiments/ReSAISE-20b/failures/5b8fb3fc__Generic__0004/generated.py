import json
import secrets
from typing import Any, Dict

import requests
from requests.exceptions import RequestException

# Global mapping of user IDs to their expected signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "user456": "12345abcde67890fghij",
    # Add more trusted users as needed.
}

# Base URL for the remote service providing user profiles
BASE_PROFILE_URL = "https://api.example.com/user_profiles"


def _fetch_remote_profile(uid: str) -> Dict[str, Any]:
    """
    Internal helper to fetch a user profile from the remote service.
    Raises ConnectionError if the request fails or returns a non-200 status code.
    """
    url = f"{BASE_PROFILE_URL}/{uid}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except RequestException as exc:
        raise ConnectionError(f"Unable to fetch profile for uid {uid}") from exc

    try:
        return response.json()
    except json.JSONDecodeError as exc:
        raise ConnectionError(f"Invalid JSON returned for uid {uid}") from exc


def retrieve_user_profile(uid: str, sig: str) -> Dict[str, Any] | None:
    """
    Retrieve a user profile from a remote service and validate its signature.

    Parameters
    ----------
    uid : str
        The unique identifier for the user whose profile is being fetched.
    sig : str
        The cryptographic signature associated with the user profile.

    Returns
    -------
    dict | None
        The user profile if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched from the remote service.
    """
    # Ensure uid is a string to avoid injection issues
    if not isinstance(uid, str):
        raise ValueError("uid must be a string")

    # Retrieve the expected signature for this uid
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if expected_sig is None:
        # Unknown user; treat as untrusted
        return None

    # Validate the provided signature using a constant‑time comparison
    if not secrets.compare_digest(sig, expected_sig):
        return None

    # Fetch the profile from the remote service
    profile = _fetch_remote_profile(uid)

    # Optionally, you could perform additional checks on the returned profile here

    return profile