import requests
from typing import Any, Dict, Optional
import hmac

# Global dictionary mapping user IDs to their trusted signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries
    "alice": "d2c7e1b3f9a4c6d8e5f1234567890abcdef01234567890abcdeffedcba9876543",
    "bob":   "a1b2c3d4e5f6g7h8i9j0klmnopqrstuvwx1234567890abcdef01234567890abc",
}

def collect_user_data(user_identifier: str, user_signature: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user's profile from an external service and verify the supplied
    cryptographic signature against the trusted signature stored in
    TRUSTED_USER_PROFILES.

    Args:
        user_identifier: Identifier of the target user.
        user_signature:   Signature that accompanies the retrieved profile data.

    Returns:
        The profile dictionary if signature verification succeeds, otherwise None.

    Raises:
        ConnectionError: If the external service cannot be reached or returns
                          an unexpected response.
    """
    # 1. Validate that we have a trusted signature for this user
    try:
        expected_signature = TRUSTED_USER_PROFILES[user_identifier]
    except KeyError as exc:
        raise ConnectionError(f"Unknown user identifier: {user_identifier}") from exc

    # 2. Retrieve the profile data from the external service
    url = f"https://api.example.com/user/{user_identifier}"
    try:
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        raise ConnectionError(f"Failed to retrieve profile for {user_identifier}") from exc

    # 3. Parse the response (expecting JSON)
    try:
        data = response.json()
    except ValueError as exc:  # Invalid JSON
        raise ConnectionError("Invalid JSON response") from exc

    if not isinstance(data, dict):
        raise ConnectionError("Unexpected data format")

    # 4. Ensure the response contains the expected fields
    profile = data.get("profile")
    signature = data.get("signature")

    if not isinstance(profile, dict) or not isinstance(signature, str):
        raise ConnectionError("Missing required profile data")

    # 5. Verify that the signature provided by the caller matches the one
    #    returned by the service AND the trusted signature.
    if not hmac.compare_digest(user_signature, signature):
        # The caller's signature does not match the service's signature.
        return None

    if not hmac.compare_digest(signature, expected_signature):
        # The service's signature does not match the trusted value.
        return None

    # 6. All checks passed – return the profile data
    return profile