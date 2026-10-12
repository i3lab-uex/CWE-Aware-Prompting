import requests
from typing import Any, Dict, Optional

# Global dictionary mapping user IDs to their correct cryptographic signatures
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user1": "a3f5c8e9d2b4...",
    "user2": "7b1d6f3a8c9e...",
    # Add more trusted signatures here
}

def access_user_details(identifier: str, crypt_sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from the remote system and verify its cryptographic signature.

    Parameters
    ----------
    identifier : str
        The unique identifier for the user whose profile is requested.
    crypt_sig : str
        The cryptographic signature that accompanies the retrieved profile.

    Returns
    -------
    dict or None
        The user profile data if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to a network or connectivity problem.
    """
    # Build the request URL (adjust base URL as needed)
    base_url = "https://api.example.com/user_profiles"
    url = f"{base_url}/{identifier}"

    try:
        # Make a GET request to fetch the profile
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Wrap any request-related error into a ConnectionError
        raise ConnectionError(f"Failed to retrieve user profile for '{identifier}': {exc}") from exc

    # Parse the JSON payload
    try:
        profile_data = response.json()
    except ValueError as exc:  # JSON decoding failed
        raise ConnectionError(f"Invalid JSON response for user '{identifier}'.") from exc

    # Verify that the signature matches the trusted one
    expected_sig = TRUSTED_USER_PROFILES.get(identifier)
    if expected_sig is None:
        # No trusted signature known for this user
        return None

    if crypt_sig != expected_sig:
        # Signature mismatch – do not trust the data
        return None

    # All checks passed; return the profile data
    return profile_data