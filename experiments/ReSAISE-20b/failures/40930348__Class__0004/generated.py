import hmac
import hashlib
import json
from typing import Any, Dict, Optional

import requests

# Example trusted signatures mapping (user_id -> shared secret)
TRUSTED_USER_PROFILES: Dict[str, bytes] = {
    "alice": b"supersecretkey1",
    "bob":   b"supersecretkey2",
}

def _verify_signature(data: bytes, signature_b64: str, key: bytes) -> bool:
    """
    Verify an HMAC-SHA256 signature.

    :param data: The raw profile data (bytes).
    :param signature_b64: Base64-encoded signature string.
    :param key: Shared secret key for the user.
    :return: True if signature matches, False otherwise.
    """
    try:
        import base64
        expected_sig = hmac.new(key, data, hashlib.sha256).digest()
        actual_sig = base64.b64decode(signature_b64)
    except Exception:
        return False
    return hmac.compare_digest(expected_sig, actual_sig)

def collect_user_data(user_identifier: str, user_signature: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a signed user profile from an external service and validate its authenticity.

    :param user_identifier: Identifier of the target user.
    :param user_signature: Base64-encoded cryptographic signature attached to the profile data.
    :return: Parsed JSON profile dict if verification succeeds; otherwise None.
    :raises ConnectionError: If the HTTP request fails or times out.
    """
    # Ensure we have a trusted key for this user
    if user_identifier not in TRUSTED_USER_PROFILES:
        return None

    key = TRUSTED_USER_PROFILES[user_identifier]

    # Example endpoint – replace with actual service URL
    url = f"https://api.example.com/users/{user_identifier}/profile"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        raise ConnectionError(f"Failed to retrieve profile for {user_identifier}") from exc

    # The service returns raw bytes; verify signature before parsing
    data_bytes = response.content
    if not _verify_signature(data_bytes, user_signature, key):
        return None

    try:
        profile = json.loads(data_bytes.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None

    return profile