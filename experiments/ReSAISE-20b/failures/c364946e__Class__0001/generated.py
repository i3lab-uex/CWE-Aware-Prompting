import json
import hmac
from typing import Any, Dict

import requests

# Global mapping of user IDs to known cryptographic signatures
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries; in a real system these would be securely stored
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "user456": "e99a18c428cb38d5f260853678922e03",
    # ...
}

def _verify_signature(user_id: str, signature: str) -> bool:
    """
    Verify that the provided signature matches the trusted one for this user.
    Uses constant‑time comparison to mitigate timing attacks.
    """
    expected = TRUSTED_USER_PROFILES.get(user_id)
    if not expected:
        return False
    # Use hmac.compare_digest for constant‑time comparison
    return hmac.compare_digest(expected, signature)

def fetch_user_profile(user_id: str, signature: str) -> Any:
    """
    Retrieve a user profile from a remote service and verify its authenticity.

    Parameters
    ----------
    user_id : str
        The unique identifier of the user whose profile needs to be fetched.
    signature : str
        The cryptographic signature accompanying the user profile data.

    Returns
    -------
    Any
        The user profile data if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the user profile could not be fetched from the remote service.
    """
    # First, perform a quick signature check against trusted signatures
    if not _verify_signature(user_id, signature):
        return None

    # Construct the request URL
    url = f"https://api.example.com/users/{user_id}/profile"

    try:
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except requests.RequestException as exc:
        # Convert all request‑related errors to a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for user {user_id}") from exc

    try:
        profile_data = response.json()
    except json.JSONDecodeError:
        # If the payload is not valid JSON, treat it as a failure
        return None

    # Optional: further validate the payload structure here if needed

    return profile_data