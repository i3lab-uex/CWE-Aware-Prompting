import hashlib
import hmac
import json
from typing import Any, Dict

# Simulated external service URL (for demonstration only)
USER_PROFILE_URL = "https://api.example.com/user/"

# Global dictionary mapping user IDs to their shared secrets (used for HMAC)
TRUSTED_USER_PROFILES: Dict[str, bytes] = {
    # uid : secret key (bytes)
    "alice": b"super_secret_key_alice",
    "bob":   b"another_secret_key_bob",
    # Add more users as needed
}


def _compute_hmac(data: bytes, key: bytes) -> str:
    """
    Compute the hexadecimal HMAC-SHA256 of *data* using *key*.
    """
    return hmac.new(key, data, hashlib.sha256).hexdigest()


def retrieve_user_data(uid: str, sig: str) -> Any | None:
    """
    Retrieve a user profile from an external service and verify its signature.

    Parameters
    ----------
    uid : str
        The user identifier whose profile is being fetched.
    sig : str
        The cryptographic signature attached to the profile data (hex string).

    Returns
    -------
    dict | None
        The user profile dictionary if the signature verification succeeds;
        otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved from the external service.
    """
    # Ensure we have a trusted secret for this user
    if uid not in TRUSTED_USER_PROFILES:
        raise ConnectionError(f"Unknown UID '{uid}'. Cannot verify signature.")

    secret_key = TRUSTED_USER_PROFILES[uid]

    # --- Step 1: Retrieve the profile data from the external service ---
    try:
        import requests
    except ImportError as exc:
        raise ConnectionError("Missing 'requests' library.") from exc

    url = f"{USER_PROFILE_URL}{uid}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except Exception as exc:
        raise ConnectionError(f"Failed to fetch profile for UID '{uid}'.") from exc

    # The external service is expected to return JSON
    try:
        profile_json = response.text.encode("utf-8")
        # Parse to ensure it's valid JSON
        json.loads(profile_json)
    except Exception as exc:
        raise ConnectionError(f"Invalid JSON received for UID '{uid}'.") from exc

    # --- Step 2: Verify the signature ---
    expected_sig = _compute_hmac(profile_json, secret_key)

    # Constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(expected_sig, sig):
        # Signature does not match; do not trust the data
        return None

    # All checks passed – parse and return the profile data
    return json.loads(profile_json)