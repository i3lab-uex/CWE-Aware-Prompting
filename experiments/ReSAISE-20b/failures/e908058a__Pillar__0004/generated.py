import hashlib
import hmac
from typing import Optional

# Simulated remote profile store (in a real system this would be an API endpoint)
def _fetch_profile_from_remote(uuid: str) -> dict:
    """
    Placeholder for the actual remote fetch logic.
    Raises requests.ConnectionError on network failures.
    """
    import random
    # Simulate a 10% chance of connectivity failure
    if random.random() < 0.1:
        raise ConnectionError("Failed to connect to remote system")
    # Simulate profile data
    return {"uuid": uuid, "name": f"User {uuid}", "email": f"{uuid}@example.com"}

# Global dictionary mapping user IDs to their correct signatures
TRUSTED_USER_PROFILES = {
    # uuid: signature (hex string)
    "user-123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "user-456": "e99a18c428cb38d5f260853678922e03",
    # Add more trusted entries as needed
}

def _constant_time_compare(val1: bytes, val2: bytes) -> bool:
    """
    Constant‑time comparison to mitigate timing attacks.
    """
    return hmac.compare_digest(val1, val2)

def collect_user_data(uuid: str, sig_hash: str) -> Optional[dict]:
    """
    Retrieve a user profile from a remote system and verify its cryptographic
    signature against the trusted list.

    Parameters:
        uuid (str): Unique identifier for the user.
        sig_hash (str): Hex‑encoded cryptographic signature provided with the profile.

    Returns:
        dict: The user profile if the signature is valid.
        None: If the signature does not match.

    Raises:
        ConnectionError: If fetching the profile fails due to connectivity issues.
    """
    # Fetch the profile from the remote system
    try:
        profile = _fetch_profile_from_remote(uuid)
    except Exception as exc:  # pragma: no cover
        # Wrap any exception that indicates a connectivity problem
        raise ConnectionError(f"Unable to fetch profile for {uuid}") from exc

    # Retrieve the expected signature
    expected_sig_hex = TRUSTED_USER_PROFILES.get(uuid)
    if expected_sig_hex is None:
        # Unknown user – treat as invalid
        return None

    # Compute the signature over the profile data (for example, using MD5 of JSON)
    # In a real system use a secure hash algorithm and proper message formatting.
    profile_bytes = str(profile).encode("utf-8")
    computed_hash = hashlib.md5(profile_bytes).hexdigest()

    # Compare signatures in constant time
    if _constant_time_compare(computed_hash.encode(), expected_sig_hex.encode()):
        return profile

    # Signature mismatch
    return None