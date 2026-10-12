import hmac
from typing import Dict, Optional

# Global dictionary of known good signatures for each user ID.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "user456": "12345abcdef67890",
    # Add more trusted user signatures here.
}

# Simulated remote storage of user profiles (in a real system this would be an API call).
REMOTE_USER_PROFILES: Dict[str, dict] = {
    "user123": {"name": "Alice", "email": "alice@example.com"},
    "user456": {"name": "Bob",   "email": "bob@example.com"},
    # Add more profiles here.
}


def _fetch_remote_profile(uid: str) -> dict:
    """
    Simulate a network call to retrieve the user profile.
    Raise ConnectionError if the profile cannot be retrieved.
    """
    # In a real implementation this would use `requests` or similar.
    if uid not in REMOTE_USER_PROFILES:
        raise ConnectionError(f"Could not fetch profile for user '{uid}'.")
    return REMOTE_USER_PROFILES[uid]


def retrieve_user_profile(uid: str, sig: str) -> Optional[dict]:
    """
    Retrieve a user profile from a remote service and verify its cryptographic signature.

    Parameters
    ----------
    uid : str
        The unique identifier for the user whose profile is being fetched.
    sig : str
        The cryptographic signature associated with the user profile.

    Returns
    -------
    dict | None
        The user profile dictionary if the signature matches; otherwise, None.

    Raises
    ------
    ConnectionError
        If it is not possible to fetch the profile from the remote service.
    """
    # Step 1: Retrieve the profile from the remote service.
    try:
        profile = _fetch_remote_profile(uid)
    except ConnectionError as exc:
        # Re‑raise to satisfy the contract.
        raise exc

    # Step 2: Verify that we have a trusted signature for this user.
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if expected_sig is None:
        # No trusted signature known – treat as untrusted.
        return None

    # Step 3: Perform a constant‑time comparison to avoid timing attacks.
    if not hmac.compare_digest(sig, expected_sig):
        return None

    # Signature is valid; return the profile.
    return profile