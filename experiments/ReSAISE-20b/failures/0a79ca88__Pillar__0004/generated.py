import json
import hmac
import hashlib
from typing import Optional, Dict

import requests
from requests.exceptions import RequestException, HTTPError

# Global mapping of user IDs to their trusted signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (user_id: signature)
    "alice": "5f2c9e1d3b6a4f7e8d0c2b4e5f9a1b3c",
    "bob":   "6a8d2e3f4b1c5d7e9f0a2b3c4d6e8f1g",
    # Add more trusted profiles as needed
}

def _fetch_profile_from_remote(u_id: str) -> Dict:
    """
    Internal helper that performs the actual HTTP GET request to fetch a user profile.
    Raises ConnectionError if any network or HTTP error occurs.

    Args:
        u_id: The unique identifier for the user.

    Returns:
        A dictionary representing the user's profile.
    """
    url = f"https://api.example.com/users/{u_id}"
    try:
        # Verify SSL certificates to prevent MITM attacks.
        response = requests.get(url, timeout=5.0, verify=True)
        response.raise_for_status()
    except (RequestException, HTTPError) as exc:
        # Wrap lower‑level exceptions into a generic ConnectionError.
        raise ConnectionError(f"Unable to fetch profile for user '{u_id}': {exc}") from exc

    try:
        return response.json()
    except json.JSONDecodeError as exc:
        # The remote service returned non‑JSON data.
        raise ConnectionError(f"Invalid JSON from profile endpoint for user '{u_id}'.") from exc

def get_user_details(u_id: str, sig_code: str) -> Optional[Dict]:
    """
    Retrieve a user profile from a remote service and validate its cryptographic signature.

    Args:
        u_id:      The unique identifier for the user whose profile is being fetched.
        sig_code:  The cryptographic signature provided with the user profile.

    Returns:
        The user profile dictionary if the signature matches the trusted value.
        None if the signature does not match.

    Raises:
        ConnectionError: If the profile cannot be fetched from the remote service.
    """
    # Basic input validation
    if not isinstance(u_id, str) or not u_id:
        raise ValueError("u_id must be a non‑empty string")
    if not isinstance(sig_code, str) or not sig_code:
        raise ValueError("sig_code must be a non‑empty string")

    # Fetch the profile from the remote service
    profile = _fetch_profile_from_remote(u_id)

    # Retrieve the expected signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(u_id)

    # If the user is not in our trusted list, we cannot validate
    if expected_sig is None:
        return None

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(sig_code, expected_sig):
        return None

    # Signature matches – trust the profile
    return profile