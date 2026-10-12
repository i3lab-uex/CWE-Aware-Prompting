import json
from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException

# Global dictionary mapping user IDs to the expected signature for their profile data
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (populate with real data in production)
    "alice": "abc123signature",
    "bob": "def456signature",
}

# Base URL of the external service providing user profiles
BASE_PROFILE_URL = "https://api.example.com/user_profiles"


def collect_user_data(user_identifier: str, user_signature: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service and verify its signature.

    Parameters
    ----------
    user_identifier : str
        Identifier for the targeted user whose profile is being fetched.
    user_signature : str
        Cryptographic signature attached to the profile data.

    Returns
    -------
    dict | None
        The user profile data if signature verification succeeds; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved due to a network or service error.
    """
    # 1. Validate that the provided signature matches the trusted one
    expected_signature = TRUSTED_USER_PROFILES.get(user_identifier)
    if expected_signature is None:
        # No trusted signature known for this user
        return None

    if user_signature != expected_signature:
        # Signature mismatch – do not trust the data
        return None

    # 2. Fetch profile from external service
    url = f"{BASE_PROFILE_URL}/{user_identifier}"
    try:
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except RequestException as exc:
        # Wrap any request-related exception in ConnectionError
        raise ConnectionError(f"Failed to retrieve profile for '{user_identifier}': {exc}") from exc

    # 3. Parse JSON response
    try:
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        # Invalid JSON – treat as a retrieval failure
        raise ConnectionError(f"Invalid JSON response for '{user_identifier}': {exc}") from exc

    # 4. Final sanity check: ensure returned data contains the expected user identifier
    if profile_data.get("id") != user_identifier:
        # Data integrity issue – signature was good but payload mismatched
        return None

    return profile_data