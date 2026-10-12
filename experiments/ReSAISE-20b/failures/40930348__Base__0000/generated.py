#!/usr/bin/env python3
"""
Utility to fetch a user profile from an external service and validate the
cryptographic signature that accompanies it.

The module intentionally uses constant‑time comparison to avoid timing attacks
(CWE-347) and raises a ConnectionError when the HTTP request fails.
"""

from __future__ import annotations

import json
import logging
import hmac
import hashlib
from typing import Any, Dict, Optional

import requests

# --------------------------------------------------------------------------- #
# Global dictionary containing the trusted signature for each user identifier
# --------------------------------------------------------------------------- #
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (hex encoded signatures)
    "alice": "5e8c9d7f2b4a1e3d6c7f8a0b9c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d",
    "bob":   "3a1b2c4d5e6f708192a3b4c5d6e7f8091a2b3c4d5e6f708192a3b4c5d6e7f809",
    # Add more trusted signatures as required
}

# --------------------------------------------------------------------------- #
# Logging configuration (adjust level or handlers as needed)
# --------------------------------------------------------------------------- #
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")


def _validate_signature(expected_sig: str, provided_sig: str) -> bool:
    """
    Compare two signatures using constant‑time comparison to mitigate
    timing attacks.

    Parameters:
        expected_sig (str): The trusted signature in hex format.
        provided_sig (str): The signature received with the profile data.

    Returns:
        bool: True if both signatures match, False otherwise.
    """
    # Ensure both are bytes; hmac.compare_digest accepts bytes or strings,
    # but using bytes guarantees consistent behaviour.
    expected_bytes = bytes.fromhex(expected_sig)
    provided_bytes = bytes.fromhex(provided_sig)

    return hmac.compare_digest(expected_bytes, provided_bytes)


def collect_user_data(user_identifier: str, user_signature: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service and validate its
    cryptographic signature.

    Parameters:
        user_identifier (str): Identifier of the target user.
        user_signature (str): Hex‑encoded cryptographic signature attached
                              to the profile data.

    Returns:
        dict: The user profile if the signature is valid.
        None: If the signature verification fails or no trusted
              signature exists for the user.

    Raises:
        ConnectionError: If the HTTP request to fetch the profile fails.
    """
    # --------------------------------------------------------------------- #
    # Step 1: Retrieve trusted signature for the user
    # --------------------------------------------------------------------- #
    expected_signature = TRUSTED_USER_PROFILES.get(user_identifier)
    if not expected_signature:
        logging.warning("No trusted signature found for user %s; rejecting data.", user_identifier)
        return None

    # --------------------------------------------------------------------- #
    # Step 2: Fetch the profile data from the external service
    # --------------------------------------------------------------------- #
    url = f"https://api.example.com/user/{user_identifier}"
    try:
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        logging.error("Failed to retrieve profile for user %s: %s", user_identifier, exc)
        raise ConnectionError(f"Unable to fetch profile for {user_identifier}") from exc

    # --------------------------------------------------------------------- #
    # Step 3: Parse JSON payload
    # --------------------------------------------------------------------- #
    try:
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        logging.error("Invalid JSON for user %s: %s", user_identifier, exc)
        return None

    # --------------------------------------------------------------------- #
    # Step 4: Verify the signature
    # --------------------------------------------------------------------- #
    if not _validate_signature(expected_signature, user_signature):
        logging.warning("Signature mismatch for user %s; data rejected.", user_identifier)
        return None

    # --------------------------------------------------------------------- #
    # Step 5: Return the verified profile
    # --------------------------------------------------------------------- #
    logging.info("Successfully validated profile for user %s.", user_identifier)
    return profile_data


# --------------------------------------------------------------------------- #
# Example usage (remove or guard with if __name__ == "__main__" in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Replace these with real identifiers and signatures for testing
    uid = "alice"
    sig = "5e8c9d7f2b4a1e3d6c7f8a0b9c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d"

    try:
        profile = collect_user_data(uid, sig)
        if profile is not None:
            print(f"Profile for {uid}: {profile}")
        else:
            print(f"Failed to validate profile for {uid}.")
    except ConnectionError as e:
        print(e)