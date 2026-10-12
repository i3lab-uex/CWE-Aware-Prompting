import hmac
import hashlib
from typing import Optional, Dict

# Global dictionary mapping user IDs to their expected signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "a1b2c3d4e5f6g7h8i9j0",
    "bob":   "0123456789abcdef1234",
    # Add more trusted user signatures here.
}

def _fetch_profile_from_remote(identifier: str) -> Dict[str, str]:
    """
    Simulate fetching a user profile from a remote system.
    In a real implementation, this would involve network I/O.
    For demonstration purposes, we return dummy data or raise a
    ConnectionError to emulate connectivity problems.
    """
    # Simulate network failure for demonstration (you can replace this logic).
    if identifier == "unreachable":
        raise ConnectionError(f"Unable to reach remote system for user '{identifier}'.")
    # Dummy profile data.
    return {"id": identifier, "name": f"User {identifier}", "email": f"{identifier}@example.com"}

def access_user_details(identifier: str, crypt_sig: str) -> Optional[Dict[str, str]]:
    """
    Fetch a user profile from a remote system and verify its cryptographic signature.

    Args:
        identifier: The unique identifier for the user whose profile is to be fetched.
        crypt_sig:  The cryptographic signature provided with the profile data.

    Returns:
        The user profile dictionary if the signature is valid; otherwise None.

    Raises:
        ConnectionError: If the remote system cannot be reached.
    """
    # 1. Retrieve the expected signature for this user from the trusted list.
    expected_sig = TRUSTED_USER_PROFILES.get(identifier)
    if not expected_sig:
        # No trusted signature known for this user; treat as invalid.
        return None

    # 2. Fetch the profile data from the remote system (may raise ConnectionError).
    try:
        profile = _fetch_profile_from_remote(identifier)
    except Exception as exc:
        # Propagate connectivity issues.
        raise ConnectionError(f"Failed to fetch profile for '{identifier}': {exc}") from exc

    # 3. Verify the provided signature against the expected one using constant‑time comparison.
    if not hmac.compare_digest(crypt_sig, expected_sig):
        # Signature mismatch – do not trust the data.
        return None

    # 4. Return the trusted profile data.
    return profile