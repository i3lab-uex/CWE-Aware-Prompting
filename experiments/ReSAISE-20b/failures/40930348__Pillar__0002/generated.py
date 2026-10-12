import json
import hmac
import logging
from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException

# Global mapping of user IDs to the expected cryptographic signatures for their
# profile data. In a real deployment this would be populated from a secure
# configuration store or environment variable.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries
    "alice": "a1b2c3d4e5f678901234567890abcdef12345678",
    "bob":   "deadbeefcafebabe00112233445566778899aabb",
}

# Base URL of the external user profile service
PROFILE_SERVICE_URL = "https://api.example.com/users"

# Configure a logger for debugging and audit purposes
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def collect_user_data(user_identifier: str, user_signature: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user's profile from an external service and verify the supplied
    cryptographic signature before trusting the data.

    Parameters
    ----------
    user_identifier : str
        Identifier for the targeted user whose profile is being fetched.
    user_signature : str
        Cryptographic signature attached to the profile data.

    Returns
    -------
    dict or None
        The user profile data if signature verification succeeds, otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved from the external service.
    """
    if not isinstance(user_identifier, str) or not isinstance(user_signature, str):
        raise TypeError("user_identifier and user_signature must be strings")

    # Retrieve the expected signature for this user from the trusted store
    expected_signature = TRUSTED_USER_PROFILES.get(user_identifier)
    if expected_signature is None:
        logger.warning("No trusted signature found for user %s", user_identifier)
        return None

    # Perform a timing‑safe comparison to avoid leaking information via
    # response time differences.
    if not hmac.compare_digest(expected_signature, user_signature):
        logger.warning("Signature mismatch for user %s", user_identifier)
        return None

    # Construct the request URL
    url = f"{PROFILE_SERVICE_URL}/{user_identifier}"

    try:
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except RequestException as exc:
        logger.error("Failed to retrieve profile for user %s: %s", user_identifier, exc)
        raise ConnectionError(f"Unable to retrieve profile for {user_identifier}") from exc

    # The service is assumed to return JSON data. If the response is not
    # valid JSON, a ValueError will be raised.
    try:
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        logger.error("Invalid JSON received for user %s: %s", user_identifier, exc)
        return None

    # Additional sanity checks on the returned data can be performed here
    if not isinstance(profile_data, dict):
        logger.warning("Profile data for user %s is not a JSON object", user_identifier)
        return None

    logger.info("Successfully retrieved and verified profile for user %s", user_identifier)
    return profile_data