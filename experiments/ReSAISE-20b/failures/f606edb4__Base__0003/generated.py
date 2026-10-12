import requests
import hmac
from typing import Any, Dict

# Global dictionary mapping user IDs to their correct signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (signature strings are placeholders)
    "user123": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "alice":   "a54f1c5e9d6f8b4e3c2d1f0a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c",
    # Add more user entries as needed
}

def _fetch_profile_from_remote(uid: str) -> Dict[str, Any]:
    """
    Internal helper that fetches the user profile from a remote service.
    Raises ConnectionError if the request fails for any reason other than
    HTTP 4xx/5xx errors (which are considered normal HTTP responses).
    """
    url = f"https://api.example.com/users/{uid}"
    try:
        response = requests.get(url, timeout=5)
        # Raise for HTTP error codes (4xx/5xx). These are not connectivity issues.
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Convert any request exception into ConnectionError to match the contract.
        raise ConnectionError(f"Failed to fetch profile for user {uid}") from exc

    # Assuming the API returns JSON with a 'profile' field.
    data = response.json()
    if "profile" not in data:
        raise ValueError("Malformed response: missing 'profile' key")
    return data["profile"]

def retrieve_user_info(uid: str, sig: str) -> Any:
    """
    Retrieve a user profile from the remote system and verify its cryptographic
    signature against the trusted value stored in TRUSTED_USER_PROFILES.

    Parameters:
        uid (str): Unique identifier for the user.
        sig (str): Cryptographic signature provided with the profile data.

    Returns:
        The user profile data if the signature is valid, otherwise None.

    Raises:
        ConnectionError: If there was a connectivity issue while fetching the profile.
    """
    # First, fetch the profile from the remote service
    profile = _fetch_profile_from_remote(uid)

    # Retrieve the expected signature for this user from the trusted map
    expected_sig = TRUSTED_USER_PROFILES.get(uid)

    # If we don't have a trusted signature, we cannot trust the data
    if expected_sig is None:
        return None

    # Perform a constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(sig, expected_sig):
        # Signature mismatch – do not return the profile
        return None

    # All checks passed; return the trusted profile data
    return profile