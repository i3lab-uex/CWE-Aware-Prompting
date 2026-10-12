import hmac
import random
from typing import Any, Dict

# Global dictionary mapping user IDs to the correct cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user1": "a1b2c3d4e5f6g7h8i9j0",
    "user2": "1234567890abcdef1234",
    # Add more trusted user signatures as needed.
}

def _fetch_remote_profile(identifier: str) -> Dict[str, Any]:
    """
    Simulate fetching a user profile from a remote system.
    In a real implementation this would perform network I/O.
    """
    # Simulate a connectivity issue with a small probability.
    if random.random() < 0.05:
        raise ConnectionError(f"Unable to connect to remote system for user {identifier}")

    # Simulated profile data; in practice this would come from the remote source.
    profiles = {
        "user1": {"name": "Alice", "email": "alice@example.com"},
        "user2": {"name": "Bob",   "email": "bob@example.com"},
    }
    return profiles.get(identifier, {})

def access_user_details(identifier: str, crypt_sig: str) -> Any:
    """
    Retrieve a user profile from a remote system and verify its cryptographic signature.

    Parameters
    ----------
    identifier : str
        The unique identifier for the user whose profile needs to be fetched.
    crypt_sig : str
        The cryptographic signature that was provided with the profile data.

    Returns
    -------
    Any
        The user profile data if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the user profile cannot be fetched due to a connectivity issue.
    """
    # Fetch the profile data from the remote system
    profile = _fetch_remote_profile(identifier)

    if not profile:
        # No profile found; treat as invalid signature
        return None

    # Retrieve the expected signature for this user from the trusted store.
    expected_sig = TRUSTED_USER_PROFILES.get(identifier)
    if not expected_sig:
        # Unknown user; cannot verify authenticity
        return None

    # Use constant‑time comparison to avoid timing attacks.
    if not hmac.compare_digest(crypt_sig, expected_sig):
        return None

    # Signature verified; return the profile data.
    return profile