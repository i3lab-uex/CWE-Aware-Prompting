import json
import random
from typing import Any, Dict

# Global dictionary mapping user IDs to their trusted signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user123": "sig_a1b2c3",
    "alice":   "sig_4d5e6f",
    "bob":     "sig_7g8h9i",
}

def _simulate_remote_fetch(identifier: str) -> Dict[str, Any]:
    """
    Simulate a remote call to fetch user profile data.

    This placeholder function randomly raises ConnectionError to mimic
    network failures. In a real implementation this would use an HTTP client.
    """
    # Simulate a 20% chance of connectivity failure
    if random.random() < 0.2:
        raise ConnectionError(f"Failed to reach remote system for user {identifier}")

    # Dummy profile data; in practice this would come from the server.
    return {
        "id": identifier,
        "name": f"Name of {identifier}",
        "email": f"{identifier}@example.com",
    }

def access_user_details(identifier: str, crypt_sig: str) -> Dict[str, Any] | None:
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
    dict | None
        The user profile data if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to connectivity issues.
    """
    # Fetch the profile data from the remote system
    profile = _simulate_remote_fetch(identifier)

    # Retrieve the expected signature for this user from the trusted dictionary
    expected_sig = TRUSTED_USER_PROFILES.get(identifier)

    # If no trusted signature exists for the user, treat it as invalid
    if expected_sig is None:
        return None

    # Compare the provided signature with the trusted one
    if crypt_sig == expected_sig:
        return profile

    # Signature mismatch; do not trust the data
    return None