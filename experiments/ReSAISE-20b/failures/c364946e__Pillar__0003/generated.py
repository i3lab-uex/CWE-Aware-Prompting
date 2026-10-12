import json
import hmac
import hashlib
from typing import Any, Dict, Optional

import requests

# Global dictionary mapping user IDs to their known cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries – in a real system these would be populated securely.
    "alice": "5f2c1a7d3e4b9c6f8a0b1234567890ab",
    "bob":   "1d4e2f3a5b6c7d8e9f01234567890abc",
}


def _verify_signature(provided_sig: str, expected_sig: str) -> bool:
    """
    Compare two signatures in constant time to mitigate timing attacks.
    """
    return hmac.compare_digest(provided_sig.encode(), expected_sig.encode())


def fetch_user_profile(user_id: str, signature: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from a remote service and verify its signature.

    Args:
        user_id: The unique identifier of the user whose profile is requested.
        signature: The cryptographic signature accompanying the retrieved data.

    Returns:
        A dictionary containing the user profile if the signature is valid,
        otherwise None.

    Raises:
        ConnectionError: If the remote service cannot be reached or returns
                          an error status code.
    """
    # Ensure we have a known expected signature for the user
    expected_sig = TRUSTED_USER_PROFILES.get(user_id)
    if not expected_sig:
        # Unknown user – we cannot trust the data
        return None

    # Verify that the provided signature matches the expected one
    if not _verify_signature(signature, expected_sig):
        return None

    # Construct the request URL – adjust base URL as needed
    url = f"https://api.example.com/users/{user_id}/profile"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        # Wrap any request‑related exception into ConnectionError
        raise ConnectionError(f"Failed to fetch profile for user {user_id}") from exc

    try:
        # Parse JSON payload safely
        profile_data = response.json()
    except json.JSONDecodeError:
        # Malformed JSON – treat as a failure
        return None

    # Additional optional checks (e.g., required fields) can be added here
    return profile_data