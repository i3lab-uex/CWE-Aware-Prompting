import json
from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException

# Global dictionary mapping user IDs to their trusted signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries; in real usage these would be populated elsewhere.
    "user123": "abcde12345signature",
    "alice":   "fghij67890signature",
}

def retrieve_user_info(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a user profile from the remote system and verify its signature.

    Parameters
    ----------
    uid : str
        The unique identifier for the user whose profile needs to be fetched.
    sig : str
        The cryptographic signature that was provided with the profile data.

    Returns
    -------
    dict or None
        The user profile as a dictionary if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to a connectivity issue.
    """
    # Ensure we have a trusted signature for the requested user
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if not expected_sig:
        # Unknown user; treat as invalid signature
        return None

    # Verify the provided signature against the trusted one
    if sig != expected_sig:
        return None

    # Construct the request URL (replace with actual endpoint)
    url = f"https://api.example.com/users/{uid}"

    # Use a session for connection pooling and set a reasonable timeout
    session = requests.Session()
    try:
        response = session.get(url, timeout=5.0)  # seconds
        response.raise_for_status()
    except RequestException as exc:
        # Wrap any requests exception into a ConnectionError
        raise ConnectionError(f"Failed to fetch user profile for {uid}") from exc

    # Parse JSON response
    try:
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        # If the payload isn't valid JSON, treat it as a connectivity problem
        raise ConnectionError(f"Invalid response format for user {uid}") from exc

    return profile_data