import hmac
import hashlib
import time
from typing import Dict, Any

# Global dictionary mapping user IDs to their correct cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (in a real system these would be securely stored).
    "user123": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "alice":   "d41d8cd98f00b204e9800998ecf8427e",
    # Add more trusted profiles as needed.
}

def _fetch_profile_from_remote(identifier: str) -> Dict[str, Any]:
    """
    Simulates a remote call to fetch user profile data.
    In real code this would use `requests` or another HTTP client.

    Raises:
        ConnectionError: If the remote system is unreachable.
    """
    # Simulate network latency
    time.sleep(0.1)

    # For demonstration, we raise ConnectionError if the identifier
    # contains "bad" to mimic a connectivity issue.
    if "bad" in identifier:
        raise ConnectionError(f"Unable to connect to remote system for user {identifier}")

    # Return a mock profile
    return {
        "id": identifier,
        "name": f"User {identifier}",
        "email": f"{identifier}@example.com",
    }

def access_user_details(identifier: str, crypt_sig: str) -> Dict[str, Any] | None:
    """
    Retrieves a user profile from a remote system and verifies the provided
    cryptographic signature against the trusted signature.

    Args:
        identifier: Unique user identifier.
        crypt_sig:  Cryptographic signature accompanying the profile data.

    Returns:
        The user profile dictionary if the signature is valid; otherwise None.

    Raises:
        ConnectionError: If the remote system cannot be reached.
    """
    # Step 1: Fetch profile from remote system
    try:
        profile = _fetch_profile_from_remote(identifier)
    except ConnectionError as exc:
        # Propagate connectivity errors
        raise

    # Step 2: Retrieve the trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(identifier)
    if not expected_sig:
        # No trusted signature known for this user
        return None

    # Step 3: Verify the signature using constant‑time comparison
    if not hmac.compare_digest(crypt_sig, expected_sig):
        return None

    # Signature is valid; return the profile
    return profile