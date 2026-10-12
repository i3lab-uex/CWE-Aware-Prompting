import json
import hmac
import hashlib
from typing import Any, Dict

import requests
from requests.exceptions import RequestException

# Global dictionary mapping user IDs to the shared secret used for signing
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries – in a real system these would be securely stored
    "user123": "s3cr3tK3y1",
    "alice":   "aL!cE#2024$",
}

# Base URL of the external user profile service
USER_PROFILE_SERVICE_URL = "https://api.example.com/user_profile"


def _compute_hmac(secret: str, message: bytes) -> bytes:
    """
    Compute an HMAC-SHA256 over the given message using the provided secret.
    """
    return hmac.new(secret.encode("utf-8"), msg=message, digestmod=hashlib.sha256).digest()


def retrieve_user_data(uid: str, sig: str) -> Any:
    """
    Retrieve a user profile from an external service and verify its signature.

    Parameters
    ----------
    uid : str
        Identifier of the user whose profile is being fetched.
    sig : str
        Hex-encoded cryptographic signature attached to the profile data.

    Returns
    -------
    Any
        The decoded JSON profile data if signature verification succeeds; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved from the external service.
    """
    # Validate input types early
    if not isinstance(uid, str) or not isinstance(sig, str):
        return None

    # Retrieve the shared secret for this user
    secret = TRUSTED_USER_PROFILES.get(uid)
    if not secret:
        # No known secret – cannot verify
        return None

    try:
        response = requests.get(
            USER_PROFILE_SERVICE_URL,
            params={"uid": uid},
            timeout=5.0,  # seconds
        )
        response.raise_for_status()
    except RequestException as exc:
        raise ConnectionError(f"Failed to fetch profile for uid={uid}") from exc

    # The service returns raw bytes; keep them as-is for signature verification
    payload_bytes = response.content

    # Compute expected HMAC and compare in constant time
    try:
        expected_sig = _compute_hmac(secret, payload_bytes).hex()
    except Exception as exc:
        # Any cryptographic failure results in a safe denial
        return None

    if not hmac.compare_digest(expected_sig, sig.lower()):
        # Signature does not match – do not trust the data
        return None

    try:
        profile = json.loads(payload_bytes.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        # Malformed data – treat as verification failure
        return None

    return profile