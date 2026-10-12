import requests
from typing import Dict, Any, Optional

# Global dictionary mapping user IDs to their trusted signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (replace with real data in production)
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "user456": "0123456789abcdef1234",
}

def _fetch_remote_profile(uid: str) -> Dict[str, Any]:
    """
    Internal helper that performs an HTTP GET request to the remote
    user‑profile service.

    Args:
        uid: The unique identifier for the user.

    Returns:
        A dictionary containing the profile data.

    Raises:
        ConnectionError: If any network problem occurs.
    """
    # Replace with the actual endpoint URL
    url = f"https://api.example.com/users/{uid}"
    try:
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except (requests.exceptions.RequestException, requests.exceptions.Timeout) as exc:
        raise ConnectionError(f"Failed to fetch profile for {uid}") from exc

    # Assume the API returns JSON
    return response.json()

def retrieve_user_info(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from a remote system and verify its signature.

    Args:
        uid: The unique identifier for the user.
        sig: The cryptographic signature provided with the profile data.

    Returns:
        The user profile dictionary if the signature is valid, otherwise None.

    Raises:
        ConnectionError: If the remote profile cannot be fetched due to connectivity issues.
    """
    # Verify that we have a trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if not expected_sig or sig != expected_sig:
        # Signature mismatch – do not trust the data
        return None

    # Fetch profile from remote system
    profile = _fetch_remote_profile(uid)

    # Optionally, perform additional checks on the returned data
    if not isinstance(profile, dict) or "id" not in profile:
        # Malformed data – treat as untrusted
        return None

    return profile