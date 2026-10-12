import hmac
import hashlib
import json
from typing import Any, Dict, Optional

# Example trusted signatures mapping (user_id -> expected signature)
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "user456": "e99a18c428cb38d5f260853678922e03",
    # Add more trusted signatures as needed
}

def _fetch_profile(identifier: str) -> Dict[str, Any]:
    """
    Simulate fetching a user profile from a remote system.
    In a real implementation this would perform an HTTP request or similar.
    """
    # For demonstration purposes, return a mock profile
    if identifier == "user123":
        return {"id": "user123", "name": "Alice", "email": "alice@example.com"}
    if identifier == "user456":
        return {"id": "user456", "name": "Bob", "email": "bob@example.com"}
    # Simulate a connectivity failure for unknown users
    raise ConnectionError(f"Unable to reach remote system for user {identifier}")

def access_user_details(identifier: str, crypt_sig: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a user profile from a remote system and verify its cryptographic signature.

    Parameters
    ----------
    identifier : str
        The unique identifier for the user whose profile needs to be fetched.
    crypt_sig : str
        The cryptographic signature that was provided with the profile data.

    Returns
    -------
    dict or None
        The user profile if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the user profile cannot be fetched due to connectivity issues.
    """
    # Fetch the profile data from the remote system
    try:
        profile = _fetch_profile(identifier)
    except Exception as exc:
        # Convert any exception into a ConnectionError for the caller
        raise ConnectionError(f"Failed to fetch profile for {identifier}") from exc

    # Retrieve the expected signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(identifier)
    if expected_sig is None:
        # Unknown user – treat as invalid
        return None

    # Use a timing‑safe comparison to avoid side‑channel attacks
    if hmac.compare_digest(expected_sig, crypt_sig):
        return profile

    # Signature mismatch – do not trust the data
    return None