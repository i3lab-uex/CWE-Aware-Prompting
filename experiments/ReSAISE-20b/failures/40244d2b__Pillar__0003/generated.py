import requests
import hmac
from typing import Optional

# Global mapping of user identifiers to their trusted signatures.
TRUSTED_USER_PROFILES = {
    # Example entries (replace with real data)
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "user456": "e99a18c428cb38d5f260853678922e03",
}

def access_user_details(identifier: str, crypt_sig: str) -> Optional[dict]:
    """
    Fetch a user profile from the remote system and verify its cryptographic signature.

    Parameters
    ----------
    identifier : str
        The unique user ID for which the profile is requested.
    crypt_sig : str
        The signature received along with the profile data.

    Returns
    -------
    dict | None
        The user profile data if the signature is valid; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved due to a network/connectivity problem.
    """
    # Construct the URL for fetching the user profile.  In a real
    # system this would be a secure HTTPS endpoint.
    url = f"https://api.example.com/users/{identifier}/profile"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Convert all request‑related errors into a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for {identifier}") from exc

    try:
        profile_data = response.json()
    except ValueError as exc:  # JSON decoding failed
        raise ConnectionError(f"Invalid response format for {identifier}") from exc

    # Retrieve the trusted signature for this user, if any.
    expected_sig = TRUSTED_USER_PROFILES.get(identifier)

    # If we have no trusted signature for this user, consider the
    # verification failed.
    if expected_sig is None:
        return None

    # Use constant‑time comparison to avoid timing attacks.
    if not hmac.compare_digest(crypt_sig, expected_sig):
        return None

    # Signature verified; return the profile data.
    return profile_data