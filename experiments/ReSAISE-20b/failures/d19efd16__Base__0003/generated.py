import requests
import hmac
from typing import Any, Dict

# Example trusted signatures dictionary (user_id -> expected signature)
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # "user123": "base64-encoded-signature",
    # Add entries as needed
}

def get_user_info(profile_id: str, profile_sig: str) -> Any | None:
    """
    Retrieve a user profile from an external service and verify its signature.

    Parameters
    ----------
    profile_id : str
        Identifier of the user whose profile is being fetched.
    profile_sig : str
        Cryptographic signature attached to the profile data.

    Returns
    -------
    dict | None
        The user profile data if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved from the external service.
    """
    # Construct the URL for fetching the user profile
    url = f"https://example.com/api/profiles/{profile_id}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        # Wrap any request-related exception in a ConnectionError
        raise ConnectionError(f"Failed to retrieve profile for {profile_id}") from exc

    # Parse the JSON payload
    try:
        profile_data = response.json()
    except ValueError as exc:
        # Invalid JSON; treat as a failed retrieval
        raise ConnectionError(f"Invalid response format for profile {profile_id}") from exc

    # Fetch the expected signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(profile_id)
    if expected_sig is None:
        # No trusted signature available; cannot verify
        return None

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(profile_sig, expected_sig):
        return None

    # Signature matches; return the profile data
    return profile_data