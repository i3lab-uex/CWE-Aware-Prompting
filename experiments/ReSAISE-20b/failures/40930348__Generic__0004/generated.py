import json
from typing import Any, Dict, Optional

import requests
from hmac import compare_digest


# Global dictionary mapping user IDs to the trusted signature for that user's profile.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries – replace with real data in production.
    "alice": "5f2c3e7b1d9a6f4e8b0c1d2e3f4a5b6c",
    "bob":   "9a8b7c6d5e4f3a2b1c0d9e8f7g6h5i4j",
}


def collect_user_data(user_identifier: str, user_signature: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a signed user profile from an external service and validate its signature.

    Parameters
    ----------
    user_identifier : str
        The identifier of the target user.
    user_signature : str
        The cryptographic signature that should match the trusted signature for this user.

    Returns
    -------
    dict | None
        The user profile data if the signature is valid; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved from the external service.
    """
    # The URL of the external service that provides user profiles.
    # Replace with the actual endpoint in a real deployment.
    PROFILE_URL = f"https://api.example.com/users/{user_identifier}/profile"

    try:
        response = requests.get(PROFILE_URL, timeout=5.0)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Wrap any network‑related exception in a ConnectionError.
        raise ConnectionError(f"Failed to retrieve profile for user '{user_identifier}': {exc}") from exc

    try:
        payload = response.json()
    except json.JSONDecodeError as exc:
        raise ConnectionError(f"Invalid JSON from profile service for user '{user_identifier}'.") from exc

    # Expected payload structure:
    # {
    #     "profile": { ... },
    #     "signature": "<hex‑encoded signature>"
    # }
    profile_data = payload.get("profile")
    returned_signature = payload.get("signature")

    if not isinstance(profile_data, dict) or not isinstance(returned_signature, str):
        # Malformed response
        return None

    # Verify that the returned signature matches the trusted one.
    expected_signature = TRUSTED_USER_PROFILES.get(user_identifier)

    if not expected_signature:
        # No trusted signature known for this user – cannot verify.
        return None

    if compare_digest(returned_signature, expected_signature) and compare_digest(user_signature, expected_signature):
        # The caller's signature also matches the trusted value – trust the data.
        return profile_data

    # Signature mismatch: do not expose any user data.
    return None