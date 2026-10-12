import hmac
import hashlib
import random
from typing import Optional

# Global mapping of trusted user IDs to their expected cryptographic signatures.
TRUSTED_USER_PROFILES = {
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "user456": "deadbeef1234567890ab",
    # Add more trusted profiles as needed.
}

def _fetch_profile_from_remote(uid: str) -> dict:
    """
    Simulate a remote fetch of a user profile.
    In a real implementation this would perform an HTTP request or similar I/O.
    Randomly raise ConnectionError to emulate network failures.
    """
    # Simulate network unreliability
    if random.random() < 0.1:   # 10% chance of failure
        raise ConnectionError(f"Unable to fetch profile for user {uid}")

    # Dummy profile data
    return {
        "uid": uid,
        "name": f"User {uid}",
        "email": f"{uid}@example.com",
    }

def retrieve_user_profile(uid: str, sig: str) -> Optional[dict]:
    """
    Retrieve a user profile from a remote service and validate its signature.

    Parameters
    ----------
    uid : str
        Unique identifier for the user.
    sig : str
        Cryptographic signature associated with the retrieved profile.

    Returns
    -------
    dict | None
        The user profile dictionary if the signature matches a trusted value;
        otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched from the remote service.
    """
    # 1. Fetch the profile; propagate ConnectionError if it occurs
    profile = _fetch_profile_from_remote(uid)

    # 2. Retrieve the expected signature for this UID
    expected_sig = TRUSTED_USER_PROFILES.get(uid)

    # 3. If no trusted signature is known, treat as untrusted
    if expected_sig is None:
        return None

    # 4. Perform a constant‑time comparison to prevent timing attacks
    if not hmac.compare_digest(sig, expected_sig):
        return None

    # 5. Signature matches; profile is considered trustworthy
    return profile

# Example usage (uncomment to test):
# try:
#     user_profile = retrieve_user_profile("user123", "a1b2c3d4e5f6g7h8i9j0")
#     if user_profile:
#         print("Trusted profile:", user_profile)
#     else:
#         print("Signature mismatch or untrusted UID.")
# except ConnectionError as e:
#     print(f"Connection error: {e}")