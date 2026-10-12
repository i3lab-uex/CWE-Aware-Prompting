import requests
import hmac
from typing import Any, Dict, Optional

# Mapping of user IDs to their trusted cryptographic signatures
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user_123": "a1b2c3d4e5f6g7h8i9j0",
    "user_456": "abcdef1234567890abcd",
    # Add more trusted signatures here
}

def fetch_user_profile(user_id: str, signature: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from a remote service and verify its signature.

    Parameters
    ----------
    user_id : str
        The unique identifier of the user whose profile needs to be fetched.
    signature : str
        The cryptographic signature accompanying the user profile data.

    Returns
    -------
    dict | None
        The user profile data if the signature is valid, otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the user profile could not be fetched from the remote service.
    """
    # 1. Fetch the profile data
    url = f"https://api.example.com/users/{user_id}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Wrap any network-related error into a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for user {user_id}") from exc

    # 2. Verify the signature
    trusted_sig = TRUSTED_USER_PROFILES.get(user_id)
    if not trusted_sig:
        # No trusted signature available for this user
        return None

    # Use constant‑time comparison to mitigate timing attacks (CWE-347)
    if not hmac.compare_digest(signature.encode(), trusted_sig.encode()):
        return None

    # 3. Return the parsed JSON profile data
    try:
        return response.json()
    except ValueError as exc:
        # If the response is not valid JSON, treat it as a failure
        raise ConnectionError(f"Invalid JSON for user {user_id}") from exc