import requests
from typing import Optional, Dict

# Global dictionary mapping user IDs to their trusted signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "abc123signature",
    "bob":   "def456signature",
    # Add more trusted users here...
}

# Base URL of the remote service that hosts user profiles.
BASE_PROFILE_URL = "https://api.example.com/user_profiles"


def fetch_profile_info(user_ident: str, user_sig: str) -> Optional[Dict]:
    """
    Retrieve a user's profile from the remote service and verify its signature.

    Parameters
    ----------
    user_ident : str
        Unique identifier for the requested user.
    user_sig : str
        Cryptographic signature that accompanies the profile.

    Returns
    -------
    dict or None
        The user profile dictionary if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the remote service cannot be reached or a network error occurs.
    """
    # Construct the URL for the specific user profile
    url = f"{BASE_PROFILE_URL}/{user_ident}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Any network or HTTP error is wrapped in a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for user '{user_ident}': {exc}") from exc

    # Parse the JSON response
    try:
        profile_data = response.json()
    except ValueError as exc:
        # Invalid JSON payload
        raise ConnectionError(f"Invalid JSON received for user '{user_ident}'.") from exc

    # Verify that the provided signature matches the trusted one
    expected_sig = TRUSTED_USER_PROFILES.get(user_ident)
    if expected_sig is None:
        # User ID not recognized as trusted
        return None

    if user_sig != expected_sig:
        # Signature mismatch: profile is not trustworthy
        return None

    # All checks passed; return the profile data
    return profile_data