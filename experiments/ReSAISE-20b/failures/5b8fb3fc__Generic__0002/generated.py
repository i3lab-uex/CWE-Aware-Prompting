import json
from typing import Dict, Any, Optional

import requests
from requests.exceptions import RequestException

# Global mapping of trusted user IDs to their expected signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (replace with real data in production)
    "user_123": "a1b2c3d4e5f6g7h8i9j0",
    "user_456": "z9y8x7w6v5u4t3s2r1q0",
    # ...
}


def retrieve_user_profile(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from the remote service and verify its cryptographic signature.

    Parameters
    ----------
    uid : str
        The unique identifier for the user whose profile is being fetched.
    sig : str
        The cryptographic signature associated with the user profile.

    Returns
    -------
    dict or None
        The user profile as a dictionary if the signature is valid.
        Returns ``None`` if the signature does not match the expected one.

    Raises
    ------
    ConnectionError
        If it is impossible to fetch the profile from the remote service.
    """
    # Step 1: Verify that we have a trusted signature for this UID
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if expected_sig is None:
        # UID not recognized – we refuse to fetch the profile
        return None

    if sig != expected_sig:
        # Signature mismatch – data is not trustworthy
        return None

    # Step 2: Build the request URL (example endpoint)
    base_url = "https://api.example.com/user_profiles"
    url = f"{base_url}/{uid}"

    try:
        # Perform the GET request with a timeout and basic safety checks
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()  # Raises HTTPError for bad status codes
    except RequestException as exc:
        # Wrap any request-related exception in a ConnectionError for clarity
        raise ConnectionError(f"Failed to fetch profile for UID {uid}") from exc

    # Step 3: Parse the JSON payload
    try:
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        raise ConnectionError(f"Invalid JSON received for UID {uid}") from exc

    # Optional: Additional sanity checks on the returned data
    if not isinstance(profile_data, dict):
        raise ConnectionError(f"Unexpected profile format for UID {uid}")

    return profile_data