import base64
import hashlib
import hmac
from typing import Any, Dict

import requests  # type: ignore[import]

# Global dictionary mapping user IDs to their HMAC secret keys
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (user_id: base64-encoded secret key)
    "alice": "c2VjcmV0X2tleV9hbGljZQ==",
    "bob":   "c2VjcmV0X2tleV9ib2I=",
    # Add more user entries here
}


def _verify_signature(profile_data: bytes, signature_b64: str, secret_key_b64: str) -> bool:
    """
    Verify that the provided base64-encoded HMAC-SHA256 signature matches
    the one computed over `profile_data` using the provided base64-encoded secret key.
    """
    try:
        secret_key = base64.b64decode(secret_key_b64)
        signature_expected = hmac.new(
            secret_key, profile_data, hashlib.sha256
        ).digest()
        signature_provided = base64.b64decode(signature_b64)
    except (ValueError, TypeError):
        # Malformed base64 or other decoding issue
        return False

    # Constant‑time comparison to mitigate timing attacks (CWE-347)
    return hmac.compare_digest(signature_expected, signature_provided)


def collect_user_data(user_identifier: str, user_signature: str) -> Any | None:
    """
    Retrieve a user profile from an external service and validate its
    cryptographic signature.

    Args:
        user_identifier: The identifier of the user whose profile to fetch.
        user_signature:  Base64-encoded HMAC-SHA256 signature attached to the profile data.

    Returns:
        The parsed JSON profile if the signature is valid; otherwise, None.

    Raises:
        ConnectionError: If there was a problem retrieving the profile from the external service.
    """
    # 1. Ensure we have a trusted secret for this user
    if user_identifier not in TRUSTED_USER_PROFILES:
        # Unknown user – cannot validate signature
        return None

    secret_key_b64 = TRUSTED_USER_PROFILES[user_identifier]

    # 2. Fetch profile data
    url = f"https://example.com/api/profiles/{user_identifier}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        raise ConnectionError(f"Failed to retrieve profile for {user_identifier}") from exc

    # 3. Verify signature
    profile_bytes = response.content
    if not _verify_signature(profile_bytes, user_signature, secret_key_b64):
        # Signature mismatch – data is not trustworthy
        return None

    # 4. Parse and return the JSON payload (assuming it is JSON)
    try:
        return response.json()
    except ValueError:
        # Malformed JSON – treat as invalid
        return None