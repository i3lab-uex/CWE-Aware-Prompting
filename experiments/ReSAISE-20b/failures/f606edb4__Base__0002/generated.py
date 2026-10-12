import requests
from hmac import compare_digest

# Example trusted signatures for demonstration purposes.
TRUSTED_USER_PROFILES = {
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "alice":   "z1x2c3v4b5n6m7l8k9j0",
    # ... add more trusted user signatures here ...
}

def retrieve_user_info(uid: str, sig: str):
    """
    Fetch a user profile from the remote system and verify its cryptographic signature.

    Parameters
    ----------
    uid : str
        Unique identifier of the user whose profile is requested.
    sig : str
        Cryptographic signature that accompanies the fetched profile data.

    Returns
    -------
    dict | None
        The user profile dictionary if the signature is valid; otherwise None.

    Raises
    ------
    ConnectionError
        If any network-related error occurs while fetching the profile.
    """
    # Validate that we have a trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if not expected_sig:
        # No trusted signature known for this user; treat as invalid
        return None

    # Compare signatures using a constant‑time comparison to mitigate timing attacks
    if not compare_digest(sig, expected_sig):
        return None

    # Build the request URL (replace with actual endpoint)
    url = f"https://api.example.com/users/{uid}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Wrap any network exception in a ConnectionError to match the spec
        raise ConnectionError(f"Failed to fetch profile for user {uid}") from exc

    try:
        profile = response.json()
    except ValueError as exc:  # JSON decoding failed
        raise ConnectionError(f"Invalid response format for user {uid}") from exc

    # At this point the signature has already been verified, so we can safely return the data
    return profile