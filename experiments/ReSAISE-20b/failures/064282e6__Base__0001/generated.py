import hashlib
import hmac
from typing import Any, Dict, Optional

import requests


# Example trusted signatures dictionary.
# In a real system this would be securely stored and probably contain
# the secret key or public key needed for signature verification.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # uid : secret_key (hex string)
    "user123": "a3f5c8d9b0e1f2... (truncated)",
    # Add more user IDs and their corresponding secret keys here.
}


def retrieve_user_data(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service and verify its cryptographic
    signature.

    Parameters
    ----------
    uid : str
        The user identifier for which the profile is requested.
    sig : str
        The cryptographic signature attached to the profile data.  It is
        expected to be a hexadecimal representation of an HMAC-SHA256 digest.

    Returns
    -------
    dict | None
        The user profile data if the signature is valid; otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the external service cannot be reached or returns an error status.
    ValueError
        If the user ID is not present in ``TRUSTED_USER_PROFILES``.
    """
    # 1. Verify we have a trusted key for this user
    if uid not in TRUSTED_USER_PROFILES:
        raise ValueError(f"Unknown UID: {uid}")

    secret_key_hex = TRUSTED_USER_PROFILES[uid]
    try:
        secret_key_bytes = bytes.fromhex(secret_key_hex)
    except ValueError as exc:
        raise ValueError(f"Invalid secret key for UID {uid}") from exc

    # 2. Retrieve the profile data
    try:
        resp = requests.get(
            f"https://example.com/api/profiles/{uid}",
            timeout=5.0,
        )
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise ConnectionError(f"Failed to retrieve profile for UID {uid}") from exc

    # 3. Parse JSON payload
    try:
        profile_data = resp.json()
    except ValueError as exc:  # includes JSONDecodeError
        raise ConnectionError(f"Invalid JSON response for UID {uid}") from exc

    # 4. Compute expected signature
    #   The payload is serialized deterministically (sorted keys) to avoid
    #   signature mismatches due to key ordering.
    payload_bytes = hashlib.sha256(
        bytes(str(sorted(profile_data.items())), encoding="utf-8")
    ).digest()

    expected_sig = hmac.new(secret_key_bytes, payload_bytes, hashlib.sha256).hexdigest()

    # 5. Compare signatures in a timing‑attack resistant way
    if not hmac.compare_digest(expected_sig, sig):
        return None

    # 6. Signature verified; return the profile data
    return profile_data