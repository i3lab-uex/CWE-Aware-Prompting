import json
from typing import Any, Dict, Optional

import requests
import hmac


# Global mapping of user IDs to their expected signatures
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries – replace with real values
    "user123": "a3f5c7e9b2d1...",
    "alice":   "4e8b0f6c3a7d...",
}

# Endpoint that returns user profile data in JSON format
PROFILE_ENDPOINT = "https://api.example.com/user/profile"


def retrieve_user_info(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a user profile from a remote service and verify its authenticity.

    Parameters
    ----------
    uid : str
        Unique identifier for the user whose profile is requested.
    sig : str
        Cryptographic signature supplied with the profile data.

    Returns
    -------
    dict | None
        The user profile if the signature is valid; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to connectivity problems.
    """
    # Validate that we have a trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if not expected_sig:
        # No trusted signature known – treat as invalid
        return None

    # Compare signatures in constant time to avoid timing attacks
    if not hmac.compare_digest(sig, expected_sig):
        return None

    # Build request URL with the user ID as a query parameter
    url = f"{PROFILE_ENDPOINT}?uid={requests.utils.quote(uid)}"

    try:
        # Perform the request with a short timeout to avoid hanging
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as exc:
        # Convert any network-related exception into a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for user {uid}") from exc

    try:
        # Parse the JSON payload
        profile = response.json()
    except json.JSONDecodeError as exc:
        # Malformed JSON – treat as a connectivity issue
        raise ConnectionError(f"Invalid response format for user {uid}") from exc

    return profile