import json
import hmac
from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException

# Global mapping of user IDs to their trusted signature (hex string)
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user123": "a1b2c3d4e5f678901234567890abcdef",
    "user456": "deadbeefcafebabe1234567890fedcba",
    # Add more trusted signatures as needed
}


def fetch_user_profile(user_id: str, signature: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from the remote service and verify its cryptographic signature.

    Args:
        user_id (str): The unique identifier of the user.
        signature (str): The cryptographic signature provided with the profile data.

    Returns:
        dict: The user profile data if the signature is valid.
        None: If the signature does not match the trusted value.

    Raises:
        ConnectionError: If the remote service cannot be reached or returns an error.
    """
    # Validate input types
    if not isinstance(user_id, str) or not isinstance(signature, str):
        raise ValueError("user_id and signature must be strings")

    # Build the request URL (example endpoint)
    url = f"https://api.example.com/users/{user_id}/profile"

    try:
        # Use a short timeout and enforce HTTPS certificate verification
        response = requests.get(url, timeout=5.0, verify=True)
        response.raise_for_status()
    except RequestException as exc:
        # Wrap any request-related error in a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for user {user_id}") from exc

    try:
        # Parse JSON payload
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        raise ValueError("Response is not valid JSON") from exc

    # Retrieve the trusted signature for this user, if known
    trusted_sig = TRUSTED_USER_PROFILES.get(user_id)
    if not trusted_sig:
        # Unknown user: treat as untrusted
        return None

    # Use constant‑time comparison to mitigate timing attacks (CWE‑693)
    if hmac.compare_digest(signature.lower(), trusted_sig.lower()):
        return profile_data

    # Signature mismatch
    return None