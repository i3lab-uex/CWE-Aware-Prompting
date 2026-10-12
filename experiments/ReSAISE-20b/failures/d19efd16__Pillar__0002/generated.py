import requests
import json
import hmac
from typing import Any, Dict, Optional

# Global dictionary mapping user IDs to the expected signature of their profile data.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (user_id: expected_signature)
    "alice": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "bob":   "a54d88e06612d820bc3be72877c74f257b561b19a8b1b2e0d5f7dd0a4c6bf1c9",
}

def get_user_info(profile_id: str, profile_sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service and verify its integrity
    using a cryptographic signature.

    Parameters:
        profile_id (str): Identifier of the user whose profile is requested.
        profile_sig (str): Signature claimed to be attached to the returned data.

    Returns:
        dict: The profile data if signature verification succeeds.
        None: If the signature does not match.

    Raises:
        ConnectionError: If the external service cannot be reached or returns
                         an unexpected status code.
    """
    # 1. Retrieve the profile data from the external service
    try:
        url = f"https://api.example.com/profiles/{profile_id}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.RequestException, ValueError) as exc:
        # Wrap any request-related failure in a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for '{profile_id}': {exc}") from exc

    try:
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        raise ConnectionError(f"Invalid JSON received for profile '{profile_id}'.") from exc

    # 2. Retrieve the expected signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(profile_id)
    if not expected_sig:
        # No trusted signature known for this user – treat as untrusted
        return None

    # 3. Verify the signature using constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(profile_sig, expected_sig):
        # Signature mismatch – do not trust the data
        return None

    # 4. All checks passed – return the profile data
    return profile_data