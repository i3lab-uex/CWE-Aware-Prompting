#!/usr/bin/env python3
"""
User profile retrieval with cryptographic signature validation.

This module demonstrates secure handling of a remote user profile
by verifying the provided signature against a trusted value.
The implementation protects against timing attacks by using
`hmac.compare_digest`, addressing CWE‑693 (Protection Mechanism Failure).
"""

from __future__ import annotations

import json
import hmac
import logging
from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException

# Configure basic logging (debug level can be adjusted as needed)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Example trusted signature store (user_id -> expected_signature).
# In a real application this would be loaded from secure storage.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user123": "f3a7c9e1b2d4e6f8a0c9b5d3e7f1a2b3",
    "alice":   "4b8c9d6e2f1a0b3c7d5e8f4a9b2c6d1",
    # ... add more trusted users
}


def get_user_details(u_id: str, sig_code: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from the remote service and validate its signature.

    Parameters
    ----------
    u_id : str
        Unique identifier for the user.
    sig_code : str
        Cryptographic signature associated with the fetched profile.

    Returns
    -------
    dict | None
        The user profile if the signature matches; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to network or service issues.
    """
    # Validate input types early
    if not isinstance(u_id, str) or not isinstance(sig_code, str):
        raise TypeError("Both u_id and sig_code must be strings")

    # Construct the remote service URL
    url = f"https://example.com/api/user/{u_id}"

    try:
        # Perform the HTTP GET with a timeout to avoid hanging
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except RequestException as exc:
        # Wrap any request-related exception into ConnectionError
        logger.error("Failed to fetch user profile for %s: %s", u_id, exc)
        raise ConnectionError(f"Unable to fetch profile for user {u_id}") from exc

    # Parse JSON payload
    try:
        profile: Dict[str, Any] = response.json()
    except json.JSONDecodeError as exc:
        logger.error("Invalid JSON from %s: %s", url, exc)
        raise ConnectionError(f"Invalid response format for user {u_id}") from exc

    # Retrieve the expected signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(u_id)
    if expected_sig is None:
        # User not in trusted list; treat as untrusted
        logger.warning("User %s is not in the trusted profile list", u_id)
        return None

    # Use constant-time comparison to avoid timing attacks
    if hmac.compare_digest(sig_code, expected_sig):
        logger.info("Signature verified for user %s", u_id)
        return profile
    else:
        logger.warning("Signature mismatch for user %s", u_id)
        return None


# Example usage (would normally be in a separate test or application file)
if __name__ == "__main__":
    try:
        user_profile = get_user_details("user123", "f3a7c9e1b2d4e6f8a0c9b5d3e7f1a2b3")
        if user_profile:
            print("Fetched profile:", user_profile)
        else:
            print("Profile could not be verified.")
    except ConnectionError as e:
        print(f"Connection error: {e}")