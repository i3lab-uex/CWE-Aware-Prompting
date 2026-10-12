import json
import base64
from typing import Optional, Dict

import requests
from requests.exceptions import RequestException

# Global mapping of user IDs to their known, trusted signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (the real values would be actual cryptographic signatures)
    "user123": "a2FubmVhbGxpZHN0b3J5",  # base64‑encoded signature
    "alice":   "c2VjcmV0dXNlcl9zaWduYXR1cmU=",
    # Add more entries as required
}


def _verify_signature(profile_data: str, signature: str) -> bool:
    """
    Simple verification that the provided signature matches the trusted one.
    In a real system this would involve cryptographic checks (e.g., RSA, ECDSA).
    Here we just compare base64‑encoded strings for demonstration.
    """
    # Normalize the signature: strip whitespace and ensure it is valid base64
    try:
        decoded_sig = base64.b64decode(signature, validate=True)
    except (base64.binascii.Error, ValueError):
        return False

    # Retrieve the trusted signature for this user
    trusted_sig_b64 = TRUSTED_USER_PROFILES.get(profile_data["user_id"])
    if not trusted_sig_b64:
        return False

    try:
        decoded_trusted = base64.b64decode(trusted_sig_b64, validate=True)
    except (base64.binascii.Error, ValueError):
        return False

    # Compare the two signatures
    return decoded_sig == decoded_trusted


def fetch_user_profile(user_id: str, signature: str) -> Optional[Dict]:
    """
    Fetches a user profile from a remote service and verifies its signature.

    Args:
        user_id (str): The unique identifier of the user.
        signature (str): The cryptographic signature accompanying the profile data.

    Returns:
        dict | None: The user profile data if the signature is valid; otherwise, None.

    Raises:
        ConnectionError: If the profile could not be retrieved from the remote service.
    """
    # Construct the request URL.  In a real implementation this would be configurable.
    url = f"https://api.example.com/users/{user_id}/profile"

    try:
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except RequestException as exc:
        # Wrap any request‑related exception in a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for user {user_id}") from exc

    try:
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        raise ConnectionError(f"Invalid JSON received for user {user_id}") from exc

    # Verify that the profile contains the expected user ID
    if profile_data.get("user_id") != user_id:
        return None

    # Verify the signature
    if not _verify_signature(profile_data, signature):
        return None

    return profile_data