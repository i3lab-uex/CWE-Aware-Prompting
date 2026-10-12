import json
import requests
from typing import Any, Dict

# Global dictionary mapping user IDs to trusted signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "sha256$abc123",
    "bob":   "sha256$def456",
    # Add more trusted user IDs and signatures here.
}

def _verify_signature(user_id: str, signature: str) -> bool:
    """
    Verify that the provided signature matches the trusted one for the user.
    Uses a constant‑time comparison to mitigate timing attacks.
    """
    trusted_sig = TRUSTED_USER_PROFILES.get(user_id)
    if not trusted_sig:
        return False
    # Constant time comparison to avoid timing side‑channels.
    if len(signature) != len(trusted_sig):
        return False
    result = 0
    for x, y in zip(signature.encode(), trusted_sig.encode()):
        result |= x ^ y
    return result == 0

def fetch_user_profile(user_id: str, signature: str) -> Any:
    """
    Retrieve a user profile from the remote service and verify its signature.

    Parameters
    ----------
    user_id : str
        The unique identifier of the user whose profile needs to be fetched.
    signature : str
        The cryptographic signature accompanying the user profile data.

    Returns
    -------
    dict | None
        The parsed JSON profile if the signature is valid, otherwise None.

    Raises
    ------
    ConnectionError
        If the profile could not be fetched from the remote service.
    """
    if not _verify_signature(user_id, signature):
        # Signature mismatch; do not trust the data.
        return None

    url = f"https://api.example.com/users/{user_id}/profile"
    try:
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        # Wrap lower‑level exceptions in ConnectionError to satisfy the spec.
        raise ConnectionError(f"Failed to fetch profile for {user_id}") from exc

    try:
        # Assume the response is JSON. If not, we treat it as invalid.
        profile_data = response.json()
    except json.JSONDecodeError:
        return None

    # Additional sanity checks can be added here (e.g., required fields).
    if not isinstance(profile_data, dict):
        return None

    return profile_data