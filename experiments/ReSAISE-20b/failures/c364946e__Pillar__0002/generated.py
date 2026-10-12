import json
import hmac
import logging
from typing import Any, Dict

import requests
from requests.exceptions import RequestException, Timeout, HTTPError

# Global mapping of user IDs to their trusted signature strings
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (to be replaced with real data)
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "user456": "e99a18c428cb38d5f260853678922e03",
}

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _verify_signature(user_id: str, signature: str) -> bool:
    """
    Verify that the supplied signature matches the trusted signature
    for the given user ID. Uses constant‑time comparison to avoid
    timing attacks (CWE-693).
    """
    trusted_sig = TRUSTED_USER_PROFILES.get(user_id)
    if not trusted_sig:
        logger.warning("No trusted signature found for user %s", user_id)
        return False
    # Constant‑time comparison
    return hmac.compare_digest(trusted_sig, signature)

def _fetch_from_remote(user_id: str) -> Dict[str, Any]:
    """
    Fetch the user profile JSON from a remote service.
    Raises ConnectionError on network or HTTP errors.
    """
    url = f"https://api.example.com/users/{user_id}/profile"
    try:
        response = requests.get(url, timeout=5.0, verify=True)
        response.raise_for_status()
    except (Timeout, RequestException) as exc:
        logger.error("Failed to fetch profile for %s: %s", user_id, exc)
        raise ConnectionError(f"Could not fetch profile for {user_id}") from exc

    try:
        return response.json()
    except json.JSONDecodeError as exc:
        logger.error("Invalid JSON from %s: %s", url, exc)
        raise ConnectionError(f"Profile data for {user_id} is not valid JSON") from exc

def fetch_user_profile(user_id: str, signature: str) -> Dict[str, Any] | None:
    """
    Retrieve a user profile from a remote service and verify its signature.

    Parameters
    ----------
    user_id : str
        The unique identifier of the user.
    signature : str
        The cryptographic signature accompanying the user profile data.

    Returns
    -------
    dict | None
        The parsed user profile if the signature is valid, otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the profile could not be fetched from the remote service.
    """
    # Verify signature before trusting any data
    if not _verify_signature(user_id, signature):
        logger.warning("Signature verification failed for user %s", user_id)
        return None

    # Fetch the profile data
    profile_data = _fetch_from_remote(user_id)
    logger.info("Successfully fetched and verified profile for user %s", user_id)
    return profile_data