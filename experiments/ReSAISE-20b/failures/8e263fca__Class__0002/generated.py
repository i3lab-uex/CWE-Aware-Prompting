import hmac
from typing import Any, Dict, Optional

# Global mapping of user IDs to their expected signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries; replace with actual trusted signatures.
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "user456": "0123456789abcdef1234",
}

def _fetch_remote_profile(user_ident: str) -> Dict[str, Any]:
    """
    Simulate fetching a user profile from a remote service.
    In a real implementation, this would perform an HTTP request or similar.

    Raises:
        ConnectionError: If the remote service is unreachable.
    """
    # Placeholder implementation – replace with real network call.
    fake_remote_database = {
        "user123": {"name": "Alice", "age": 30},
        "user456": {"name": "Bob",   "age": 25},
    }

    if user_ident not in fake_remote_database:
        # Simulate a network failure or non‑existent resource.
        raise ConnectionError(f"Could not retrieve profile for {user_ident}")

    return fake_remote_database[user_ident]


def fetch_profile_info(user_ident: str, user_sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from a remote service and verify its authenticity.

    Args:
        user_ident: The unique identifier of the user.
        user_sig:   Cryptographic signature provided with the profile.

    Returns:
        The user profile dictionary if the signature matches a trusted
        signature; otherwise, None.

    Raises:
        ConnectionError: If the profile cannot be fetched from the remote service.
    """
    # 1. Retrieve the expected signature for this user, if any.
    expected_sig = TRUSTED_USER_PROFILES.get(user_ident)
    if not expected_sig:
        # Unknown user – cannot trust any profile.
        return None

    # 2. Verify the provided signature against the expected one using
    # constant‑time comparison to mitigate timing attacks.
    if not hmac.compare_digest(user_sig, expected_sig):
        # Signature mismatch – treat the profile as untrustworthy.
        return None

    # 3. Fetch the actual profile from the remote service.
    try:
        profile = _fetch_remote_profile(user_ident)
    except ConnectionError as exc:
        # Propagate connection errors to the caller.
        raise exc

    # 4. Return the verified profile.
    return profile