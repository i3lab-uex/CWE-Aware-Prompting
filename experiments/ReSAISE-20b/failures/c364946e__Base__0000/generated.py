import json
import hmac
import hashlib
import requests
from typing import Any, Dict

# Global dictionary mapping user IDs to their known cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (replace with real data in production)
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "user456": "1234567890abcdef1234",
}

def fetch_user_profile(user_id: str, signature: str) -> Any:
    """
    Fetch a user profile from a remote service and verify its cryptographic signature.

    Args:
        user_id (str): Unique identifier of the user.
        signature (str): Cryptographic signature accompanying the profile data.

    Returns:
        Any: The parsed user profile data if the signature is valid, otherwise None.

    Raises:
        ConnectionError: If the remote service could not be reached or returned an error.
    """
    # Validate that we have a known signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(user_id)
    if expected_sig is None:
        # No known signature; treat as untrusted
        return None

    # Use a constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(signature, expected_sig):
        return None

    # URL for the remote service (placeholder)
    url = f"https://api.example.com/users/{user_id}/profile"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.exceptions.RequestException, requests.exceptions.Timeout) as exc:
        raise ConnectionError(f"Failed to fetch profile for user {user_id}") from exc

    try:
        profile_data = response.json()
    except json.JSONDecodeError:
        # If the payload is not valid JSON, treat as a failure
        return None

    # Optionally: perform additional schema validation here.

    return profile_data