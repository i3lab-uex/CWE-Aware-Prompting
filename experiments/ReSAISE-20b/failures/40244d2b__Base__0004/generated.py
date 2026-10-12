import hmac
import json
from typing import Any, Dict, Optional

# Simulated trusted signatures for user profiles.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "user456": "0123456789abcdef1234",
}

# Simulated remote service endpoint.
REMOTE_USER_PROFILES: Dict[str, Dict[str, Any]] = {
    "user123": {"name": "Alice", "email": "alice@example.com"},
    "user456": {"name": "Bob",   "email": "bob@example.com"},
}


def _fetch_remote_profile(identifier: str) -> Dict[str, Any]:
    """
    Simulates fetching a user profile from a remote system.
    Raises ConnectionError to mimic connectivity problems.
    """
    # In a real implementation this would involve an HTTP request, e.g. using `requests`.
    # Here we simply look up a pre‑defined dictionary.
    if identifier not in REMOTE_USER_PROFILES:
        # Simulate a network failure for unknown users.
        raise ConnectionError(f"Unable to fetch profile for {identifier}")
    return REMOTE_USER_PROFILES[identifier]


def access_user_details(identifier: str, crypt_sig: str) -> Optional[Dict[str, Any]]:
    """
    Fetches a user profile from a remote system and verifies its cryptographic signature.

    Args:
        identifier: The unique user ID.
        crypt_sig:  The cryptographic signature provided with the profile data.

    Returns:
        The user profile dictionary if the signature is valid; otherwise None.

    Raises:
        ConnectionError: If the remote profile cannot be retrieved due to connectivity issues.
    """
    # Step 1: Retrieve the profile data from the remote system.
    try:
        profile = _fetch_remote_profile(identifier)
    except ConnectionError as e:
        # Propagate the connectivity error.
        raise

    # Step 2: Retrieve the expected signature from the trusted source.
    expected_sig = TRUSTED_USER_PROFILES.get(identifier)
    if expected_sig is None:
        # No trusted signature available; treat as invalid.
        return None

    # Step 3: Verify the provided signature against the expected one.
    # Use constant‑time comparison to avoid timing attacks.
    if not hmac.compare_digest(crypt_sig, expected_sig):
        return None

    # Signature is valid; return the profile data.
    return profile