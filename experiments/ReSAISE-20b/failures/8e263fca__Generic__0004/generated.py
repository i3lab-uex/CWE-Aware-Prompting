import requests
from typing import Optional, Dict

# Global dictionary mapping user IDs to their expected signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries; in real usage these would be populated elsewhere.
    "user123": "abcd1234efgh5678",
    "alice":   "a1b2c3d4e5f6g7h8",
    # ... more trusted profiles ...
}

# Base URL of the remote service that provides user profiles.
BASE_PROFILE_URL = "https://api.example.com/user_profiles"


def fetch_profile_info(user_ident: str, user_sig: str) -> Optional[dict]:
    """
    Retrieve a user profile from a remote service and validate its signature.

    Parameters
    ----------
    user_ident : str
        The unique identifier for the user whose profile is being fetched.
    user_sig : str
        The cryptographic signature associated with the user profile.

    Returns
    -------
    dict | None
        The user profile dictionary if the signature is valid; otherwise `None`.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched from the remote service.
    """
    # Validate that we have a trusted signature for this user first.
    expected_sig = TRUSTED_USER_PROFILES.get(user_ident)
    if expected_sig is None:
        # Unknown user – we cannot trust the signature.
        return None

    if user_sig != expected_sig:
        # Signature does not match the trusted value.
        return None

    # Construct the URL to fetch the profile.
    url = f"{BASE_PROFILE_URL}/{user_ident}"
    try:
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as exc:
        # Wrap any request-related error in a ConnectionError for clarity.
        raise ConnectionError(f"Failed to fetch profile for user {user_ident}") from exc

    try:
        profile = response.json()
    except ValueError as exc:  # JSON decoding failed
        raise ConnectionError(f"Invalid JSON response for user {user_ident}") from exc

    # Optionally, perform additional validation on the profile structure here.
    return profile