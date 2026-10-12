import requests
import hmac
from typing import Any, Dict, Optional

# Global mapping of user IDs to the expected cryptographic signature.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user1": "a1b2c3d4e5f6g7h8i9j0",
    "user2": "1234567890abcdef0123",
    # Add more trusted user signatures here.
}

def retrieve_user_info(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a user profile from a remote system and verify its signature.

    Parameters
    ----------
    uid : str
        The unique identifier of the user.
    sig : str
        The cryptographic signature provided with the profile data.

    Returns
    -------
    dict | None
        The user profile data if the signature is valid, otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to a connectivity issue.
    """
    # Construct the request URL. In a real system this would be configurable.
    url = f"https://example.com/api/users/{uid}"

    try:
        # Retrieve the user profile. Assume the API returns JSON.
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        # Any network or HTTP error is treated as a connectivity issue.
        raise ConnectionError(f"Failed to fetch profile for user {uid}") from exc

    # Parse the JSON payload.
    try:
        profile_data = response.json()
    except ValueError as exc:  # JSON decoding failed
        raise ConnectionError(f"Invalid JSON response for user {uid}") from exc

    # Retrieve the expected signature for this user.
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if expected_sig is None:
        # No trusted signature known for this user – treat as invalid.
        return None

    # Use constant‑time comparison to avoid timing attacks (CWE‑347 mitigation).
    if not hmac.compare_digest(sig, expected_sig):
        return None

    # Signature is valid; return the profile data.
    return profile_data