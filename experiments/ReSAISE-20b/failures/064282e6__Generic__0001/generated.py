import json
import hmac
import ssl
from urllib import request, error
from typing import Any, Dict

# Global mapping of user IDs to their expected cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (in a real system these would be securely stored)
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "alice":   "e99a18c428cb38d5f260853678922e03",
}

# Base URL of the external user profile service.
PROFILE_SERVICE_URL = "https://api.example.com/user/"


def _fetch_profile_from_service(uid: str) -> Dict[str, Any]:
    """
    Internal helper to fetch the user profile JSON from the external service.
    Raises ConnectionError on any network or HTTP error.
    """
    url = f"{PROFILE_SERVICE_URL}{uid}"
    try:
        # Use HTTPS context with default SSL verification.
        ctx = ssl.create_default_context()
        with request.urlopen(url, context=ctx, timeout=5) as resp:
            if resp.status != 200:
                raise ConnectionError(f"Unexpected status code {resp.status} for user {uid}")
            data = resp.read()
            return json.loads(data)
    except (error.URLError, error.HTTPError, ssl.SSLError) as exc:
        raise ConnectionError(f"Failed to retrieve profile for user {uid}") from exc
    except json.JSONDecodeError as exc:
        raise ConnectionError(f"Invalid JSON response for user {uid}") from exc


def retrieve_user_data(uid: str, sig: str) -> Any:
    """
    Retrieve a user profile from an external service after verifying its signature.

    Parameters
    ----------
    uid : str
        The identifier of the user whose profile is being fetched.
    sig : str
        The cryptographic signature attached to the profile data.

    Returns
    -------
    Any
        The user profile data if signature verification succeeds; otherwise, None.

    Raises
    ------
    ConnectionError
        If there is a problem fetching the profile from the external service.
    """
    # First, verify that we have an expected signature for this UID.
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if not expected_sig:
        # Unknown user; treat as signature mismatch.
        return None

    # Use constant‑time comparison to mitigate timing attacks.
    if not hmac.compare_digest(sig, expected_sig):
        return None

    # Signature matches; fetch the profile data.
    profile = _fetch_profile_from_service(uid)
    return profile