import json
import hmac
import hashlib
from typing import Any, Dict, Optional

import requests  # pip install requests

# Global mapping of user identifiers to their expected signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries:
    # "user123": "5f2c3a4b8e9d... (hex digest)",
    # ...
}

def _verify_signature(user_id: str, provided_sig: str) -> bool:
    """
    Compare the supplied signature against the trusted one for *user_id*.
    The comparison is performed in constant time to mitigate timing attacks.

    Args:
        user_id: Identifier of the user.
        provided_sig: Signature supplied by the external service.

    Returns:
        True if signatures match, False otherwise.
    """
    expected_sig = TRUSTED_USER_PROFILES.get(user_id)
    if not expected_sig:
        # No trusted signature available for this user.
        return False
    # Use constant‑time comparison to avoid timing attacks (CWE-693).
    return hmac.compare_digest(expected_sig.encode(), provided_sig.encode())


def collect_user_data(user_identifier: str, user_signature: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service and validate its signature.

    Args:
        user_identifier: The ID of the target user.
        user_signature: Cryptographic signature attached to the profile data.

    Returns:
        The parsed JSON profile if verification succeeds; otherwise None.

    Raises:
        ConnectionError: If the HTTP request to fetch the profile fails.
    """
    # Validate signature first.  If it doesn't match, do not even make the request.
    if not _verify_signature(user_identifier, user_signature):
        return None

    # Construct the URL for fetching the profile.  In a real system this would be
    # an environment variable or configuration value.
    profile_url = f"https://api.example.com/users/{user_identifier}/profile"

    try:
        response = requests.get(profile_url, timeout=5)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        # Wrap lower‑level errors in ConnectionError for clarity.
        raise ConnectionError(f"Failed to retrieve profile for {user_identifier}") from exc

    try:
        # Assume the service returns JSON.  If not, parsing will raise a ValueError.
        profile_data = response.json()
    except json.JSONDecodeError:
        # Invalid JSON payload; treat as a failure to retrieve.
        raise ConnectionError(f"Invalid JSON response for {user_identifier}")

    return profile_data