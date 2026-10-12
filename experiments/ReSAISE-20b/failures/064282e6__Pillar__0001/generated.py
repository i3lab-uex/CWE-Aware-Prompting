#!/usr/bin/env python3
"""
Module providing user profile retrieval with signature verification.

The global dictionary TRUSTED_USER_PROFILES maps a user ID to the
expected cryptographic signature for that user's profile data.
"""

from __future__ import annotations

import json
import hmac
import logging
from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException

# Configure a logger for this module
logger = logging.getLogger(__name__)

# Example trusted signatures dictionary. In a real application this would
# be populated from a secure source such as an environment variable,
# configuration file, or external key‑management service.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # uid : expected_signature
    "user123": "a1b2c3d4e5f6g7h8i9j0",
    "user456": "12345abcde67890fghij",
}


def retrieve_user_data(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service and verify its
    signature against the trusted value.

    Parameters
    ----------
    uid : str
        Identifier of the target user.
    sig : str
        Cryptographic signature attached to the profile data.

    Returns
    -------
    dict | None
        The user profile data if signature verification succeeds;
        otherwise, ``None`` is returned.

    Raises
    ------
    ConnectionError
        If the HTTP request to fetch the profile fails for any reason.
    """
    # ------------------------------------------------------------------
    # 1. Retrieve user profile from the external service
    # ------------------------------------------------------------------
    api_url = f"https://api.example.com/users/{uid}"
    try:
        response = requests.get(api_url, timeout=5.0)
        response.raise_for_status()
    except RequestException as exc:
        logger.error("Failed to retrieve profile for uid=%s: %s", uid, exc)
        raise ConnectionError(f"Unable to retrieve user profile for {uid}") from exc

    # Parse the JSON payload
    try:
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        logger.error("Invalid JSON from profile endpoint for uid=%s: %s", uid, exc)
        raise ConnectionError(f"Invalid JSON response for {uid}") from exc

    # ------------------------------------------------------------------
    # 2. Verify the provided signature
    # ------------------------------------------------------------------
    expected_sig = TRUSTED_USER_PROFILES.get(uid)
    if expected_sig is None:
        logger.warning("No trusted signature found for uid=%s", uid)
        return None

    # Use constant‑time comparison to mitigate timing attacks (CWE-693)
    if not hmac.compare_digest(sig, expected_sig):
        logger.warning("Signature mismatch for uid=%s", uid)
        return None

    # ------------------------------------------------------------------
    # 3. Return the verified profile data
    # ------------------------------------------------------------------
    return profile_data


# ----------------------------------------------------------------------
# Example usage (would normally be in a separate test module)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    test_uid = "user123"
    # In a real scenario the signature would be provided by the caller
    test_sig = TRUSTED_USER_PROFILES[test_uid]

    try:
        profile = retrieve_user_data(test_uid, test_sig)
        if profile is not None:
            print("Profile retrieved successfully:")
            print(profile)
        else:
            print("Signature verification failed.")
    except ConnectionError as e:
        print(f"Connection error: {e}")