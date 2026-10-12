import json
import requests
from typing import Any, Dict, Optional

# Example trusted signatures mapping.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "a1b2c3d4e5f6g7h8i9j0",
    "bob":   "1a2b3c4d5e6f7g8h9i0j",
    # Add more user IDs and their expected signatures here.
}

def retrieve_user_info(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from the remote system and verify its cryptographic
    signature.

    Parameters:
        uid (str): The unique identifier of the user.
        sig (str): The cryptographic signature provided with the profile data.

    Returns:
        dict: The user profile if the signature is valid.
        None: If the signature does not match or the user is unknown.

    Raises:
        ConnectionError: If a network-related error occurs while fetching the profile.
    """
    # 1. Fetch the user profile from a remote endpoint
    url = f"https://api.example.com/users/{uid}"
    try:
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Wrap any network or HTTP error in a ConnectionError
        raise ConnectionError(f"Unable to fetch user profile for {uid}") from exc

    # 2. Parse the JSON payload
    try:
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        # If the payload is not valid JSON, treat it as a connectivity issue
        raise ConnectionError(f"Invalid JSON response for user {uid}") from exc

    # 3. Verify the signature
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if not expected_sig:
        # Unknown user: treat as invalid signature
        return None

    # Use constant‑time comparison to avoid timing attacks
    if not _constant_time_compare(sig, expected_sig):
        return None

    # 4. Return the verified profile
    return profile_data


def _constant_time_compare(a: str, b: str) -> bool:
    """
    Compare two strings in constant time to mitigate timing attacks.
    Python's hmac.compare_digest works for both bytes and str.
    """
    import hmac
    try:
        return hmac.compare_digest(a, b)
    except Exception:
        # Fallback: simple equality if compare_digest fails
        return a == b