import json
import hmac
from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException

# Global mapping of user IDs to known valid signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (replace with real data in production)
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "alice":   "e99a18c428cb38d5f260853678922e03",
    # ...
}

def fetch_user_profile(user_id: str, signature: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a user profile from a remote service and verify its authenticity.

    Parameters
    ----------
    user_id : str
        Unique identifier of the user whose profile is requested.
    signature : str
        Cryptographic signature accompanying the profile data.

    Returns
    -------
    dict or None
        The user profile data if the signature is verified; otherwise None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched from the remote service.
    """
    # Verify that we have a trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(user_id)
    if not expected_sig:
        # No trusted signature known for this user
        return None

    # Use constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(signature, expected_sig):
        return None

    # Build the URL for the remote service
    url = f"https://api.example.com/users/{user_id}/profile"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except RequestException as exc:
        # Wrap lower‑level request errors in a ConnectionError
        raise ConnectionError(f"Could not fetch profile for user {user_id}") from exc

    try:
        profile = response.json()
    except json.JSONDecodeError:
        # Invalid JSON payload – treat as a failure
        return None

    return profile