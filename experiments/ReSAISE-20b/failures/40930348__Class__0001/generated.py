import json
import hmac
import hashlib
from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException

# Global dictionary mapping user IDs to their HMAC secret keys.
TRUSTED_USER_PROFILES: Dict[str, bytes] = {
    # Example entries; in real usage these would be securely stored.
    "alice": b"supersecretkey_alice",
    "bob":   b"anothersecret_bob",
}


def _verify_signature(data: bytes, signature_hex: str, secret_key: bytes) -> bool:
    """
    Verify that the provided hex signature matches the HMAC-SHA256
    of *data* using *secret_key*. Uses constant‑time comparison.
    """
    try:
        expected = hmac.new(secret_key, data, hashlib.sha256).hexdigest()
    except Exception:
        return False
    # Constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected, signature_hex)


def collect_user_data(user_identifier: str, user_signature: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service and verify its authenticity.

    Parameters
    ----------
    user_identifier : str
        The identifier of the user whose profile is to be fetched.
    user_signature : str
        Hex‑encoded cryptographic signature attached to the profile data.

    Returns
    -------
    dict or None
        The user profile as a dictionary if signature verification succeeds;
        otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved from the external service.
    """
    # Ensure we have a trusted secret key for this user
    if user_identifier not in TRUSTED_USER_PROFILES:
        # No trusted key -> cannot verify
        return None

    secret_key = TRUSTED_USER_PROFILES[user_identifier]

    # Construct the URL for fetching the profile.
    # In a real system this would be configurable; here we use a placeholder.
    url = f"https://api.example.com/users/{user_identifier}/profile"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except RequestException as exc:
        # Wrap any network/HTTP errors in ConnectionError
        raise ConnectionError(f"Failed to retrieve profile for user '{user_identifier}'.") from exc

    # Profile data is expected to be JSON; encode it back to bytes for signature verification.
    try:
        profile_bytes = response.content
        # Verify the signature before decoding JSON to avoid processing tampered data.
        if not _verify_signature(profile_bytes, user_signature, secret_key):
            return None

        # Decode JSON only after signature verification.
        profile = json.loads(profile_bytes.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        # Malformed JSON or decoding issues
        return None

    return profile