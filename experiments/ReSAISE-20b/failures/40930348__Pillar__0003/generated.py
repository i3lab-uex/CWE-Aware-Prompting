#!/usr/bin/env python3
"""
collect_user_data module

This module implements the `collect_user_data` function which retrieves a user
profile from an external service, verifies its cryptographic signature against
a trusted list of signatures and returns the profile data if validation succeeds.
"""

from __future__ import annotations

import json
import hmac
import hashlib
import logging
from typing import Any, Dict, Optional

import requests  # pip install requests

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Example trusted signatures mapping.
# In a real system this would be populated from a secure source
# (e.g., a signed manifest, HSM, or encrypted config).
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # user_id : base64-encoded HMAC-SHA256 signature of the JSON profile
    "alice": "3J6rM7sZtO9Xk1lG2q4YhP5c6W7n8K0v",
    "bob":   "1a2b3c4d5e6f7g8h9i0jklmnopqrstu",
}

# Base URL of the external service that hosts user profiles
PROFILE_SERVICE_BASE_URL = "https://api.example.com/profiles"

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _fetch_profile(user_id: str) -> Dict[str, Any]:
    """
    Retrieve the user profile JSON from the external service.

    Raises:
        ConnectionError: If the HTTP request fails or returns a non-200 status.
    """
    url = f"{PROFILE_SERVICE_BASE_URL}/{user_id}"
    try:
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        log.error("Failed to retrieve profile for user %s: %s", user_id, exc)
        raise ConnectionError(f"Unable to retrieve profile for {user_id}") from exc

    try:
        return response.json()
    except json.JSONDecodeError as exc:
        log.error("Invalid JSON for user %s: %s", user_id, exc)
        raise ConnectionError(f"Invalid JSON response for {user_id}") from exc


def _verify_signature(profile: Dict[str, Any], signature_b64: str) -> bool:
    """
    Verify the HMAC-SHA256 signature of the profile data.

    The function uses a constant-time comparison to mitigate timing attacks.
    """
    # Re-serialize the profile deterministically
    profile_bytes = json.dumps(profile, sort_keys=True, separators=(",", ":")).encode("utf-8")

    # Compute HMAC with a secret key.
    # In production, the key must be stored securely (e.g., HSM or KMS).
    # For demonstration, we use a hardcoded key (insecure in real life).
    SECRET_KEY = b"super-secret-key"

    computed_hmac = hmac.new(SECRET_KEY, profile_bytes, hashlib.sha256).hexdigest()

    # Constant-time comparison
    return hmac.compare_digest(computed_hmac, signature_b64)


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def collect_user_data(user_identifier: str, user_signature: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile and validate its signature.

    Args:
        user_identifier: The identifier of the target user.
        user_signature:  The cryptographic signature attached to the profile data.

    Returns:
        The user profile dictionary if verification succeeds; otherwise None.

    Raises:
        ConnectionError: If the profile cannot be retrieved from the external service.
    """
    # Fetch the profile data
    profile = _fetch_profile(user_identifier)

    # Validate signature against trusted mapping
    expected_signature = TRUSTED_USER_PROFILES.get(user_identifier)
    if not expected_signature:
        log.warning("No trusted signature found for user %s", user_identifier)
        return None

    # Compare the provided signature with the expected one
    if not hmac.compare_digest(user_signature, expected_signature):
        log.warning("Signature mismatch for user %s", user_identifier)
        return None

    # Verify the signature over the profile content
    if not _verify_signature(profile, user_signature):
        log.warning("Computed signature does not match for user %s", user_identifier)
        return None

    # All checks passed
    log.info("Profile for user %s verified successfully", user_identifier)
    return profile

# --------------------------------------------------------------------------- #
# Example usage (for manual testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        user_id = "alice"
        # In practice, this would be supplied by the caller
        provided_sig = TRUSTED_USER_PROFILES[user_id]
        profile_data = collect_user_data(user_id, provided_sig)
        if profile_data:
            print(f"Retrieved profile for {user_id}:")
            print(json.dumps(profile_data, indent=2))
        else:
            print(f"Failed to verify profile for {user_id}.")
    except ConnectionError as e:
        print(f"Connection error: {e}")