import json
from typing import Any, Dict, Optional

import requests
from urllib.parse import urlencode, urljoin


# Global mapping of user IDs to their trusted profile signatures
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "e3b0c44298fc1c149afbf4c8996fb924",
    "bob":   "9f86d081884c7d659a2feaa0c55ad015",
    # ... add more trusted signatures as needed
}

# Base URL of the remote service that hosts user profiles
BASE_URL = "https://api.example.com/user_profiles/"


def fetch_user_profile(user_id: str, signature: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from the remote service and verify its signature.

    Parameters
    ----------
    user_id : str
        Unique identifier of the user whose profile is to be fetched.
    signature : str
        Cryptographic signature accompanying the retrieved profile data.

    Returns
    -------
    dict | None
        The user profile data if the signature is valid, otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the profile could not be fetched from the remote service.
    """
    # Construct the request URL
    url = urljoin(BASE_URL, f"{user_id}.json")

    try:
        response = requests.get(url, timeout=5.0, verify=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Wrap any request-related exception into a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for user {user_id}") from exc

    try:
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        # If the payload is not valid JSON, treat it as a fetch failure
        raise ConnectionError(f"Invalid JSON response for user {user_id}") from exc

    # Verify that the signature matches the trusted one
    expected_signature = TRUSTED_USER_PROFILES.get(user_id)
    if not expected_signature or signature != expected_signature:
        # Signature mismatch: do not trust the data
        return None

    return profile_data