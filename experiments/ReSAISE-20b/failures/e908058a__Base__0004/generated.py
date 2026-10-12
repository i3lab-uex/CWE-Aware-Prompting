import json
from typing import Optional

import hmac
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError as ReqConnectionError

# Global dictionary mapping user IDs to their correct signatures
TRUSTED_USER_PROFILES = {
    # Example entries:
    "user-123": "a1b2c3d4e5f6g7h8i9j0",
    "user-456": "1a2b3c4d5e6f7g8h9i0j",
    # Add real entries as needed
}


def _fetch_profile_from_remote(uuid: str) -> dict:
    """
    Internal helper that performs the actual HTTP GET request to retrieve
    the user profile.  The endpoint and headers are placeholders and should
    be replaced with real values in a production environment.
    """
    url = f"https://api.example.com/user/{uuid}"
    headers = {"Accept": "application/json"}
    # 5‑second timeout to avoid hanging
    response = requests.get(url, headers=headers, timeout=5)
    # Raise for HTTP errors (4xx/5xx)
    response.raise_for_status()
    return response.json()


def collect_user_data(uuid: str, sig_hash: str) -> Optional[dict]:
    """
    Fetch a user profile from a remote system and verify its cryptographic
    signature before returning the data.

    Parameters
    ----------
    uuid : str
        The unique identifier for the user whose profile needs to be fetched.
    sig_hash : str
        The cryptographic signature that was provided with the profile data.

    Returns
    -------
    dict | None
        The user profile data if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the user profile cannot be fetched due to connectivity issues.
    """
    try:
        profile = _fetch_profile_from_remote(uuid)
    except (ReqConnectionError, Timeout) as exc:
        # Re‑raise as the specified exception type
        raise ConnectionError(f"Failed to fetch profile for user {uuid}") from exc
    except RequestException as exc:
        # Other request‑related errors (e.g., HTTP 4xx/5xx)
        raise ConnectionError(f"HTTP error when fetching profile for user {uuid}") from exc

    # Verify that the signature matches the trusted value.
    # Use constant‑time comparison to avoid timing attacks (CWE‑347).
    trusted_sig = TRUSTED_USER_PROFILES.get(uuid)
    if not trusted_sig:
        # No trusted signature for this user; treat as invalid
        return None

    if not hmac.compare_digest(sig_hash, trusted_sig):
        # Signature mismatch
        return None

    return profile