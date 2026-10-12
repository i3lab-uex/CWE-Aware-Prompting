import hmac
import requests
from typing import Any, Dict, Optional

# Global mapping of user IDs to their expected cryptographic signatures
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "5f2c3e1a9b8d4c6e7f0a1b2c3d4e5f6g",
    "bob":   "9a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p",
    # Add more trusted users here
}

# Base URL of the remote profile service (example)
PROFILE_SERVICE_URL = "https://api.example.com/user_profiles"


def fetch_profile_info(user_ident: str, user_sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user's profile from the remote service and verify its signature.

    Parameters
    ----------
    user_ident : str
        The unique identifier of the user whose profile is being fetched.
    user_sig : str
        The cryptographic signature provided for the retrieved profile.

    Returns
    -------
    dict | None
        The user profile dictionary if the signature matches a trusted entry;
        otherwise, ``None`` is returned.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to network or service errors.
    """
    # Verify that we have a trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(user_ident)
    if not expected_sig:
        # Unknown user; treat as untrusted
        return None

    # Perform a constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(user_sig, expected_sig):
        return None

    # Build the request URL
    url = f"{PROFILE_SERVICE_URL}/{user_ident}"

    try:
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except (requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError) as exc:
        # Wrap any request‑related exception in a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for user '{user_ident}': {exc}") from exc

    # Parse JSON response
    try:
        profile = response.json()
    except ValueError as exc:
        # Malformed JSON is treated as a connection failure
        raise ConnectionError(f"Invalid response format for user '{user_ident}': {exc}") from exc

    # Optionally, further validation of the profile structure can be added here.

    return profile