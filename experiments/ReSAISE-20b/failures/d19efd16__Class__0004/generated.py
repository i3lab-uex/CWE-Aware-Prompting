import hashlib
import hmac
import json
from typing import Any, Dict

import requests
from requests.exceptions import RequestException

# Global dictionary mapping user IDs to their HMAC secret keys (hex strings).
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (in practice these would be securely stored).
    "user123": "4f3a9d2c1e6b8f7e0d2a1c4b5e9f3a7d",
    "alice":   "a1b2c3d4e5f60718293b4c5d6e7f8091",
}

def _verify_signature(data: bytes, signature_hex: str, secret_key_hex: str) -> bool:
    """
    Verify that the provided HMAC-SHA256 signature matches the data
    using the given secret key. Comparison is done in constant time.
    """
    try:
        secret_key = bytes.fromhex(secret_key_hex)
        expected_sig = hmac.new(secret_key, data, hashlib.sha256).digest()
    except Exception:
        # Any error in key conversion or hashing should result in failure.
        return False

    try:
        provided_sig = bytes.fromhex(signature_hex)
    except ValueError:
        return False

    # Constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected_sig, provided_sig)

def get_user_info(profile_id: str, profile_sig: str) -> Any | None:
    """
    Retrieve a user profile from an external service and verify its
    authenticity using the provided cryptographic signature.

    Parameters:
        profile_id (str): Identifier of the user whose profile is requested.
        profile_sig (str): Hexadecimal HMAC‑SHA256 signature of the profile data.

    Returns:
        The decoded JSON profile if the signature is valid, otherwise None.

    Raises:
        ConnectionError: If the external service cannot be reached or
                          returns an unexpected status code.
    """
    # Ensure we have a trusted secret key for this user
    if profile_id not in TRUSTED_USER_PROFILES:
        return None

    secret_key_hex = TRUSTED_USER_PROFILES[profile_id]

    # Example endpoint – replace with the actual service URL
    url = f"https://api.example.com/profiles/{profile_id}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except RequestException as exc:
        # Wrap any request‑related exception in a ConnectionError
        raise ConnectionError(f"Failed to retrieve profile for {profile_id}") from exc

    # The raw content is used for signature verification
    data_bytes = response.content

    if not _verify_signature(data_bytes, profile_sig, secret_key_hex):
        # Signature mismatch – treat as untrusted data
        return None

    try:
        profile = json.loads(data_bytes)
    except json.JSONDecodeError:
        # Malformed JSON – treat as failure
        return None

    return profile