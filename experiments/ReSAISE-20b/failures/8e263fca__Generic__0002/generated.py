import requests
from typing import Optional, Dict

# Global mapping of user IDs to their expected cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries; replace with actual trusted signatures.
    "alice": "SIG_ALICE_12345",
    "bob":   "SIG_BOB_67890",
}

def fetch_profile_info(user_ident: str, user_sig: str) -> Optional[Dict]:
    """
    Retrieve a user profile from a remote service and verify its cryptographic signature.

    Parameters
    ----------
    user_ident : str
        The unique identifier for the user whose profile is being fetched.
    user_sig : str
        The cryptographic signature associated with the retrieved profile.

    Returns
    -------
    dict or None
        The user profile if the signature matches an expected trusted signature;
        otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched from the remote service.
    """
    # URL of the remote service; adjust as needed.
    url = f"https://api.example.com/users/{user_ident}/profile"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        # Any network-related error results in a ConnectionError.
        raise ConnectionError(f"Failed to fetch profile for user '{user_ident}'.") from exc

    try:
        profile = response.json()
    except ValueError as exc:  # includes JSONDecodeError
        raise ConnectionError(f"Invalid JSON response for user '{user_ident}'.") from exc

    # Verify that the signature matches what we trust.
    expected_sig = TRUSTED_USER_PROFILES.get(user_ident)
    if expected_sig is None:
        # No trusted signature known for this user.
        return None

    if user_sig != expected_sig:
        # Signature mismatch; profile is not trustworthy.
        return None

    return profile