import json
from typing import Any, Dict, Optional

# Simulated global mapping of user IDs to their trusted signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user123": "sig_abc123",
    "alice":   "sig_def456",
    "bob":     "sig_ghi789",
}

def _fetch_profile_from_remote(identifier: str) -> Dict[str, Any]:
    """
    Simulated remote fetch. In a real implementation this would
    perform an HTTP request to the user profile service.
    
    Raises:
        ConnectionError: If the remote system is unreachable.
    """
    # Placeholder implementation. Replace with actual network code.
    simulated_profiles = {
        "user123": {"name": "John Doe",   "email": "john@example.com"},
        "alice":   {"name": "Alice Smith","email": "alice@example.com"},
        "bob":     {"name": "Bob Jones",  "email": "bob@example.com"},
    }
    
    if identifier not in simulated_profiles:
        # Simulate a connectivity issue for unknown users
        raise ConnectionError(f"Unable to fetch profile for {identifier}")
    
    return simulated_profiles[identifier]

def access_user_details(identifier: str, crypt_sig: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a user profile from the remote system and verify its cryptographic signature.

    Args:
        identifier: The unique user ID.
        crypt_sig:  The cryptographic signature provided with the profile data.

    Returns:
        The user profile dictionary if the signature is valid, otherwise None.

    Raises:
        ConnectionError: If the remote system cannot be reached.
    """
    try:
        profile = _fetch_profile_from_remote(identifier)
    except Exception as exc:
        # Treat any exception from the fetch as a connectivity problem.
        raise ConnectionError(f"Failed to retrieve profile for {identifier}") from exc

    expected_sig = TRUSTED_USER_PROFILES.get(identifier)
    if expected_sig is None:
        # No trusted signature known for this user; reject the profile.
        return None

    if crypt_sig != expected_sig:
        # Signature mismatch; do not trust the data.
        return None

    return profile