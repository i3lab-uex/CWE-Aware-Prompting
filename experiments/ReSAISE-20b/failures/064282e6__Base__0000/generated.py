import requests
import hmac
import hashlib
import json
from typing import Any, Dict

# Global dictionary mapping user IDs to their shared HMAC secret keys.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (in a real system these would be securely stored)
    "user123": "s3cr3tK3yForUser123",
    "alice":   "anotherSecretKey!",
}

def _compute_hmac(secret: str, data: bytes) -> str:
    """
    Compute a SHA‑256 HMAC of the given data using the provided secret key.
    Returns the hexadecimal representation of the digest.
    """
    return hmac.new(secret.encode("utf-8"), data, hashlib.sha256).hexdigest()

def retrieve_user_data(uid: str, sig: str) -> Any | None:
    """
    Retrieve a user profile from an external service and verify its
    cryptographic signature.

    Parameters:
        uid (str): Identifier of the target user.
        sig (str): Hexadecimal HMAC signature attached to the profile data.

    Returns:
        The decoded JSON profile if verification succeeds; otherwise, None.

    Raises:
        ConnectionError: If the external service cannot be reached or
                         returns a non‑200 status code.
    """
    # 1. Verify that we have a trusted secret for this user
    if uid not in TRUSTED_USER_PROFILES:
        # Unknown user – cannot verify signature
        return None

    secret_key = TRUSTED_USER_PROFILES[uid]

    # 2. Fetch the profile from the external service
    try:
        response = requests.get(
            f"https://api.example.com/users/{uid}/profile",
            timeout=5.0,  # seconds
        )
    except requests.RequestException as exc:
        raise ConnectionError(f"Failed to connect to the profile service: {exc}") from exc

    if response.status_code != 200:
        raise ConnectionError(
            f"Profile service returned unexpected status {response.status_code}"
        )

    profile_bytes = response.content

    # 3. Compute HMAC of the received data
    expected_sig = _compute_hmac(secret_key, profile_bytes)

    # 4. Compare signatures in constant time
    if not hmac.compare_digest(expected_sig, sig):
        # Signature mismatch – reject data
        return None

    # 5. Parse and return the JSON payload
    try:
        return json.loads(profile_bytes.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        # Malformed data – treat as verification failure
        return None