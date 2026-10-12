import json
from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException, Timeout, ConnectionError as ReqConnectionError

# Example trusted signatures (user_id -> expected signature)
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user123": "5f2d8e4b1c6a9e3d7f0b2a4c5e6d7f8a",
    "alice":   "3b1c4d5e6f7a8b9c0d1e2f3a4b5c6d7e",
    # Add more user IDs and their expected signatures here
}


def get_user_info(profile_id: str, profile_sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service and verify its signature.

    Parameters
    ----------
    profile_id : str
        Identifier for the targeted user whose profile is being fetched.
    profile_sig : str
        Cryptographic signature attached to the profile data.

    Returns
    -------
    dict | None
        The user profile data if signature verification is successful,
        otherwise None.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved from the external service.
    """
    # Verify that we have a trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(profile_id)
    if not expected_sig:
        # No trusted signature known for this user; reject immediately
        return None

    if profile_sig != expected_sig:
        # Signature mismatch – do not trust the data
        return None

    # Build request URL (replace with actual service endpoint)
    url = f"https://api.example.com/profiles/{profile_id}"

    try:
        # Use a short timeout to avoid hanging
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (ReqConnectionError, Timeout) as exc:
        # Convert requests exceptions to ConnectionError
        raise ConnectionError(f"Failed to retrieve profile for '{profile_id}': {exc}") from exc
    except RequestException as exc:
        # Any other requests exception also considered a connection failure
        raise ConnectionError(f"Unexpected error retrieving profile for '{profile_id}': {exc}") from exc

    try:
        # Assume the service returns JSON
        profile_data = response.json()
    except json.JSONDecodeError:
        # Invalid JSON – treat as a failure to retrieve valid data
        raise ConnectionError(f"Invalid JSON response for profile '{profile_id}'")

    return profile_data