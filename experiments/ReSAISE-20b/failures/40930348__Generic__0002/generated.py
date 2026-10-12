import hashlib
import json
from typing import Any, Dict, Optional

import requests

# Global dictionary mapping user IDs to the expected SHA‑256 signature of
# their profile JSON representation (hex encoded).
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries
    "alice": "3f5b1c7e2a9d4e8b6c1234567890abcdef1234567890abcdef1234567890abcd",
    "bob":   "1a2b3c4d5e6f7g8h9i0j1234567890abcdef1234567890abcdef1234567890ab",
    # Add more trusted users here...
}


def _verify_signature(data: bytes, expected_sig_hex: str) -> bool:
    """
    Verify that the SHA‑256 hash of `data` matches `expected_sig_hex`.
    The comparison is done in constant time to mitigate timing attacks.
    """
    # Compute SHA‑256 hash of the data
    actual_sig = hashlib.sha256(data).hexdigest()

    # Constant‑time comparison
    return hashlib.compare_digest(actual_sig, expected_sig_hex)


def collect_user_data(user_identifier: str, user_signature: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user's profile from an external service and validate its
    cryptographic signature.

    Parameters
    ----------
    user_identifier : str
        Identifier of the target user.
    user_signature : str
        Signature provided alongside the profile data (hex encoded).

    Returns
    -------
    dict or None
        The user profile JSON decoded as a dictionary if the signature is valid.
        Returns ``None`` if the signature does not match the trusted value.

    Raises
    ------
    ConnectionError
        If there is a network problem or the external service returns an error.
    """
    # Construct the request URL.  In a real implementation this would
    # likely come from configuration.
    url = f"https://api.example.com/users/{user_identifier}"

    try:
        # Perform the HTTP GET request with a timeout.
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        # Wrap any network-related exception in a ConnectionError.
        raise ConnectionError(f"Failed to retrieve profile for user '{user_identifier}'") from exc

    # Retrieve raw bytes of the response content
    profile_bytes = response.content

    # Ensure that we have a trusted signature for this user.
    expected_sig_hex = TRUSTED_USER_PROFILES.get(user_identifier)
    if not expected_sig_hex:
        # If the user is not in the trusted list, we consider it untrusted.
        return None

    # Verify that the provided signature matches what we expect.
    if not _verify_signature(profile_bytes, expected_sig_hex):
        # Signature mismatch: do not trust the data.
        return None

    try:
        # Parse JSON payload
        profile_data = json.loads(profile_bytes.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        # Malformed JSON; treat as untrusted.
        return None

    # Optional: further validation of the profile structure can be added here.

    return profile_data