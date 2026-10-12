import json
import logging
from typing import Any, Dict

import requests

# Global dictionary mapping user IDs to their expected signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries; replace with real data in production.
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "user456": "0123456789abcdef0123",
}

# Configure a basic logger for debugging purposes.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def retrieve_user_info(uid: str, sig: str) -> Any:
    """
    Fetch a user profile from a remote service and verify its cryptographic signature.

    Parameters
    ----------
    uid : str
        The unique identifier of the user whose profile is to be retrieved.
    sig : str
        The cryptographic signature accompanying the profile data.

    Returns
    -------
    Any
        The decoded JSON payload if the signature is valid; otherwise None.

    Raises
    ------
    ConnectionError
        If any network-related issue occurs while attempting to fetch the profile.
    """
    # Verify that we have a known signature for this user before making any request
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if expected_sig is None:
        logger.warning("Unknown user ID: %s", uid)
        return None

    if sig != expected_sig:
        logger.warning("Signature mismatch for user %s: received=%s, expected=%s", uid, sig, expected_sig)
        return None

    # Build the request URL.  In a real system this would be a configurable endpoint.
    url = f"https://api.example.com/users/{uid}/profile"

    try:
        # Timeout after 5 seconds; SSL verification is enabled by default.
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError) as exc:
        # Convert any requests-related exception to a ConnectionError
        logger.error("Failed to retrieve profile for user %s: %s", uid, exc)
        raise ConnectionError(f"Unable to fetch profile for user {uid}") from exc

    try:
        # Parse the JSON payload.  This could raise ValueError if invalid JSON.
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        logger.error("Invalid JSON received for user %s: %s", uid, exc)
        return None

    # Optionally perform additional validation on the profile data here.
    logger.info("Successfully retrieved and verified profile for user %s", uid)
    return profile_data