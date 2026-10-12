import json
import requests
import hmac
from typing import Optional, Dict

# Global dictionary containing trusted signatures for each user profile.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries
    "user_123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "user_456": "e99a18c428cb38d5f260853678922e03",
    # ... populate with real data
}

def fetch_user_profile(user_id: str, signature: str) -> Optional[Dict]:
    """
    Retrieve a user profile from the remote service and verify its authenticity.

    Parameters
    ----------
    user_id : str
        Unique identifier of the user.
    signature : str
        Cryptographic signature accompanying the profile data.

    Returns
    -------
    dict | None
        The user profile data if the signature is valid, otherwise None.

    Raises
    ------
    ConnectionError
        If the user profile could not be fetched from the remote service.
    """
    # URL of the remote service; adjust as needed
    url = f"https://api.example.com/users/{user_id}/profile"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        # Wrap any request-related exception in a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for user {user_id}") from exc

    # Parse the JSON payload
    try:
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        # If the payload is not valid JSON, treat it as an invalid fetch
        raise ConnectionError(f"Invalid response format for user {user_id}") from exc

    # Verify that the signature matches the trusted one
    expected_sig = TRUSTED_USER_PROFILES.get(user_id)
    if not expected_sig:
        # No trusted signature known for this user; treat as untrusted
        return None

    # Use constant-time comparison to avoid timing attacks
    if not hmac.compare_digest(signature, expected_sig):
        return None

    # If all checks pass, return the profile data
    return profile_data