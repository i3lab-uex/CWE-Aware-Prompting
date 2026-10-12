import requests
import hmac
from typing import Any, Dict, Optional

# Global mapping of user IDs to their trusted signature (hex string)
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries – in a real system these would be securely stored
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "alice":   "2c1743a391305fbf367df8e4f069f9f9",
    # ...
}

def fetch_user_profile(user_id: str, signature: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a user profile from the remote service and verify its cryptographic
    signature against a trusted value.

    Parameters
    ----------
    user_id : str
        Unique identifier of the user.
    signature : str
        Hex-encoded cryptographic signature accompanying the profile data.

    Returns
    -------
    dict or None
        The user profile dictionary if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile could not be retrieved from the remote service.
    """
    # 1. Retrieve the trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(user_id)
    if not expected_sig:
        # No trusted signature known – we cannot verify
        return None

    # 2. Verify the provided signature matches the trusted one using a constant‑time comparison
    if not hmac.compare_digest(signature.lower(), expected_sig.lower()):
        return None

    # 3. Fetch the profile data from the remote service
    url = f"https://api.example.com/users/{user_id}/profile"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        # Wrap any network/HTTP error in a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for user {user_id}") from exc

    # 4. Parse the JSON payload
    try:
        profile_data = resp.json()
    except ValueError as exc:  # includes JSONDecodeError
        raise ConnectionError(f"Invalid JSON response for user {user_id}") from exc

    # 5. Return the profile data
    return profile_data