import hmac
import hashlib
from typing import Dict, Any, Optional

# Global mapping of user IDs to their trusted signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries – replace with real data in production
    "user_123": "a1b2c3d4e5f6g7h8i9j0",
    "user_456": "123abc456def789ghi0",
}

# Simulated remote storage of user profiles.
_REMOTE_PROFILES: Dict[str, Dict[str, Any]] = {
    "user_123": {"name": "Alice", "email": "alice@example.com"},
    "user_456": {"name": "Bob",   "email": "bob@example.com"},
}


def _fetch_remote_profile(u_id: str) -> Dict[str, Any]:
    """
    Simulate fetching a user profile from a remote service.
    In a real implementation this would perform an HTTP request or
    database query. If the user ID is unknown, a ConnectionError
    is raised to mimic network or service failure.
    """
    if u_id not in _REMOTE_PROFILES:
        # Mimic network/service failure for unknown IDs
        raise ConnectionError(f"Unable to retrieve profile for {u_id}")
    return _REMOTE_PROFILES[u_id]


def get_user_details(u_id: str, sig_code: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from a remote service and validate its
    cryptographic signature.

    Args:
        u_id (str): The unique identifier for the user.
        sig_code (str): The cryptographic signature provided by the caller.

    Returns:
        dict: The user profile if the signature matches the trusted value.
        None: If the signature does not match.

    Raises:
        ConnectionError: If the remote profile cannot be fetched.
    """
    # 1. Fetch the profile from the remote service
    try:
        profile = _fetch_remote_profile(u_id)
    except Exception as exc:  # pragma: no cover
        raise ConnectionError(f"Failed to fetch profile for {u_id}") from exc

    # 2. Retrieve the expected signature
    expected_sig = TRUSTED_USER_PROFILES.get(u_id)
    if expected_sig is None:
        # No trusted signature for this user – treat as untrusted
        return None

    # 3. Perform a constant‑time comparison to prevent timing attacks.
    # Use the same hash algorithm that produced `sig_code` (here we
    # assume hex-encoded SHA256).
    try:
        expected_bytes = bytes.fromhex(expected_sig)
        provided_bytes = bytes.fromhex(sig_code)
    except ValueError:  # pragma: no cover
        # Invalid hex input – treat as untrusted
        return None

    if not hmac.compare_digest(expected_bytes, provided_bytes):
        # Signature mismatch
        return None

    # 4. Signature verified – return the profile
    return profile


# Example usage (for demonstration only)
if __name__ == "__main__":
    try:
        user_profile = get_user_details("user_123", "a1b2c3d4e5f6g7h8i9j0")
        print("Profile:", user_profile)
    except ConnectionError as e:
        print("Connection error:", e)