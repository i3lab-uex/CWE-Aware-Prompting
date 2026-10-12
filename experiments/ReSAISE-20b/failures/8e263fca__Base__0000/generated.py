import hmac
from typing import Dict, Any

# Global registry of trusted signatures for user profiles.
# In a real application this would be stored securely (e.g. in a database or
# a secrets manager).  The values here are just illustrative placeholders.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "alice": "f4b9c2d8e1a3b7f6",
    "bob":   "9a4c3d5e2f1b0a7c",
    # add more trusted users here
}

def _fetch_remote_profile(user_ident: str) -> Dict[str, Any]:
    """
    Simulated remote service call to fetch a user profile.
    In production this would perform an HTTP request or other I/O operation.

    Raises:
        ConnectionError: If the remote service cannot be reached.
    """
    # Placeholder implementation.  Replace with real network code.
    fake_remote_data = {
        "alice": {"name": "Alice Smith", "email": "alice@example.com"},
        "bob":   {"name": "Bob Jones",   "email": "bob@example.com"},
    }

    if user_ident not in fake_remote_data:
        raise ConnectionError(f"Unable to fetch profile for {user_ident}")

    return fake_remote_data[user_ident]


def fetch_profile_info(user_ident: str, user_sig: str) -> Dict[str, Any] | None:
    """
    Retrieve a user profile from the remote service and validate its
    cryptographic signature against the trusted registry.

    Args:
        user_ident: Unique identifier for the user.
        user_sig:   Cryptographic signature provided with the profile.

    Returns:
        The user profile dictionary if the signature matches; otherwise None.

    Raises:
        ConnectionError: If the remote service cannot be reached.
    """
    # 1. Retrieve profile from remote source
    profile = _fetch_remote_profile(user_ident)

    # 2. Retrieve the expected signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(user_ident)

    # 3. If no trusted signature exists, treat as untrusted
    if expected_sig is None:
        return None

    # 4. Perform a constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(user_sig, expected_sig):
        return None

    # 5. Signature verified – return the profile
    return profile