import requests
from hmac import compare_digest
from typing import Any, Dict

# Global mapping of user IDs to their trusted cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (in a real system these would be securely stored)
    "user-123": "a1b2c3d4e5f6g7h8i9j0",
    "user-456": "0123456789abcdef0123",
}

def collect_user_data(uuid: str, sig_hash: str) -> Any:
    """
    Fetch a user profile from the remote system and verify its signature.

    Parameters
    ----------
    uuid : str
        Unique identifier of the user whose profile should be fetched.
    sig_hash : str
        Cryptographic signature that accompanies the returned data.

    Returns
    -------
    Any
        The parsed profile data if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved due to a network or connectivity issue.
    """
    # Verify that we have a trusted signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(uuid)
    if expected_sig is None:
        # Unknown user – treat as invalid signature
        return None

    if not compare_digest(sig_hash, expected_sig):
        # Signature does not match
        return None

    # Build the request URL (replace with your actual endpoint)
    url = f"https://api.example.com/users/{uuid}/profile"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Convert any request-related exception into a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for user {uuid}") from exc

    try:
        return response.json()
    except ValueError as exc:
        # Invalid JSON – treat as a connectivity/formatting issue
        raise ConnectionError(f"Invalid response format for user {uuid}") from exc