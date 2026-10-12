import hmac
from typing import Optional, Dict

# Global dictionaries simulating remote service data and trusted signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "5f4dcc3b5aa765d61d8327deb882cf99",
    "bob":   "e99a18c428cb38d5f260853678922e03",
    # Add more trusted users here.
}

# Simulated remote profiles. In a real system this would be fetched via HTTP, DB query, etc.
REMOTE_USER_PROFILES: Dict[str, Dict] = {
    "alice": {"name": "Alice",   "age": 30},
    "bob":   {"name": "Bob",     "age": 25},
    # Add more remote profiles here.
}


def _fetch_remote_profile(u_id: str) -> Dict:
    """
    Simulate fetching a user profile from a remote service.
    Raises ConnectionError if the profile cannot be retrieved.
    """
    # In a real implementation this might involve network I/O. Here we simply look up the dict.
    try:
        profile = REMOTE_USER_PROFILES[u_id]
    except KeyError as exc:
        # Simulate network or service failure.
        raise ConnectionError(f"Unable to fetch profile for user '{u_id}'.") from exc
    return profile


def get_user_details(u_id: str, sig_code: str) -> Optional[Dict]:
    """
    Retrieve a user profile and verify its authenticity using the provided signature.

    Parameters
    ----------
    u_id : str
        The unique identifier of the user.
    sig_code : str
        Cryptographic signature claimed to be valid for this user's profile.

    Returns
    -------
    dict or None
        The user profile dictionary if the signature matches; otherwise None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched from the remote service.
    """
    # 1. Verify that the signature matches what we trust for this user.
    expected_sig = TRUSTED_USER_PROFILES.get(u_id)
    if expected_sig is None:
        # No trusted signature known for this user; treat as invalid.
        return None

    # Use constant‑time comparison to mitigate timing attacks (CWE-345 concern).
    if not hmac.compare_digest(sig_code, expected_sig):
        return None

    # 2. Fetch the profile from the remote service.
    profile = _fetch_remote_profile(u_id)

    # 3. Return the profile (already verified).
    return profile