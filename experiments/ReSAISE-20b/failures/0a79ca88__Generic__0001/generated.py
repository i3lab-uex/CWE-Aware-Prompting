import json
import hmac
import hashlib
from typing import Optional, Dict

import requests

# Global mapping of user IDs to their trusted cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "alice":   "abcdef1234567890fedcba",
}

# Base URL of the remote service that hosts user profiles.
USER_PROFILE_ENDPOINT = "https://api.example.com/user/profile"


def _fetch_profile_from_remote(u_id: str) -> Dict:
    """
    Internal helper that retrieves the raw profile JSON from the remote service.
    Raises ConnectionError if the request fails or returns a non‑200 status code.
    """
    try:
        response = requests.get(
            USER_PROFILE_ENDPOINT,
            params={"u_id": u_id},
            timeout=5.0,  # seconds
        )
    except requests.RequestException as exc:
        raise ConnectionError(f"Unable to reach remote service: {exc}") from exc

    if response.status_code != 200:
        raise ConnectionError(
            f"Remote service returned status {response.status_code} for user {u_id}"
        )

    try:
        return response.json()
    except json.JSONDecodeError as exc:
        raise ConnectionError(f"Invalid JSON from remote service: {exc}") from exc


def get_user_details(u_id: str, sig_code: str) -> Optional[Dict]:
    """
    Retrieve a user profile from the remote service and validate its signature.

    Parameters
    ----------
    u_id : str
        Unique identifier of the user whose profile is requested.
    sig_code : str
        Cryptographic signature provided alongside the request.

    Returns
    -------
    dict | None
        The user profile dictionary if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched from the remote service.
    """
    # 1. Retrieve the expected signature for this user, if any.
    expected_sig = TRUSTED_USER_PROFILES.get(u_id)
    if not expected_sig:
        # No trusted signature exists for this user; consider it untrusted.
        return None

    # 2. Verify that the provided signature matches the expected one using a
    #    constant‑time comparison to mitigate timing attacks.
    if not hmac.compare_digest(sig_code, expected_sig):
        # Signature does not match; reject the profile.
        return None

    # 3. Fetch the profile from the remote service.
    profile = _fetch_profile_from_remote(u_id)

    # 4. Optionally, you could perform additional checks here (e.g., schema validation).

    return profile