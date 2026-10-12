import requests
import hmac
from typing import Any, Dict, Optional

# Global mapping of user IDs to their correct cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "user456": "6f1ed002ab5595859014ebf0951522d9",
    # ... add more as needed
}

def retrieve_user_info(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from the remote system and verify its authenticity.

    Parameters
    ----------
    uid : str
        The unique identifier for the user whose profile needs to be fetched.
    sig : str
        The cryptographic signature that was provided with the profile data.

    Returns
    -------
    dict or None
        The user profile data if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to a connectivity issue.
    """
    # 1. Verify that we have a trusted signature for this UID
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if not expected_sig:
        # No known trusted signature for this user – treat as invalid
        return None

    # 2. Perform a constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(sig, expected_sig):
        return None

    # 3. Fetch the profile data from the remote system
    url = f"https://api.example.com/users/{uid}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.exceptions.RequestException, requests.exceptions.Timeout) as exc:
        # Wrap any network‑related exception in a ConnectionError
        raise ConnectionError(f"Failed to retrieve profile for user {uid}") from exc

    # 4. Return the parsed JSON data
    try:
        return response.json()
    except ValueError as exc:
        # Invalid JSON – treat as a connectivity/content issue
        raise ConnectionError(f"Invalid response format for user {uid}") from exc