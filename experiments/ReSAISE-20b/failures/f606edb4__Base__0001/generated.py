import requests
from typing import Optional, Dict

# Example trusted signatures mapping (user_id -> expected signature)
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "user456": "1234567890abcdef1234",
    # Add more trusted user IDs and their signatures here
}

def retrieve_user_info(uid: str, sig: str) -> Optional[Dict]:
    """
    Retrieve a user profile from a remote system and verify its cryptographic signature.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    sig : str
        Cryptographic signature accompanying the profile data.

    Returns
    -------
    dict or None
        The user profile if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to connectivity issues.
    """
    # Verify that we have a trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if not expected_sig:
        # Unknown user – treat as untrusted
        return None

    # The signature must match the expected one; otherwise, reject
    if sig != expected_sig:
        return None

    # Construct the URL for fetching user data (placeholder)
    url = f"https://api.example.com/users/{uid}"

    try:
        # Perform the HTTP GET request
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        # Any connectivity or HTTP error should be reported
        raise ConnectionError(f"Failed to retrieve user profile for {uid}") from exc

    # Parse JSON response
    try:
        profile_data = response.json()
    except ValueError as exc:
        # Malformed JSON – treat as a connectivity/format issue
        raise ConnectionError(f"Invalid response format for user {uid}") from exc

    return profile_data