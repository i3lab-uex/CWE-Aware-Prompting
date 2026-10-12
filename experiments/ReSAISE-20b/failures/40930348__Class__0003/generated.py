#!/usr/bin/env python3
"""
Collect a user profile from an external service and verify its authenticity.
"""

import json
import hmac
import hashlib
from typing import Any, Dict, Optional

import requests  # pip install requests

# --------------------------------------------------------------------------- #
# Global dictionary mapping user identifiers to the shared secret used for
# HMAC signing of their profile data.  In a real system this would be derived
# from a public/private key pair or an asymmetric signature scheme.
#
# Example:
#   TRUSTED_USER_PROFILES = {
#       "alice": b"super_secret_key_for_alice",
#       "bob":   b"another_very_long_secret"
#   }
#
# The secret is stored as bytes because the HMAC functions expect a byte
# sequence.  Keys should be generated securely and kept confidential.
TRUSTED_USER_PROFILES: Dict[str, bytes] = {
    # Example data – replace with real secrets in production
    "alice": b"super_secret_key_for_alice",
    "bob":   b"another_very_long_secret"
}

# --------------------------------------------------------------------------- #
def _compute_hmac(profile_bytes: bytes, secret: bytes) -> str:
    """
    Compute a hex-encoded HMAC-SHA256 of the profile data using the provided
    secret.  This helper keeps the signature logic isolated and testable.
    """
    digest = hmac.new(secret, profile_bytes, hashlib.sha256)
    return digest.hexdigest()


def collect_user_data(user_identifier: str, user_signature: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service and verify that the
    provided cryptographic signature matches the expected value.

    Parameters
    ----------
    user_identifier : str
        The identifier of the target user.
    user_signature : str
        The hex-encoded HMAC-SHA256 signature attached to the profile data.

    Returns
    -------
    dict | None
        The parsed JSON user profile if the signature is valid; otherwise,
        ``None``.  A :class:`ConnectionError` is raised if the external
        request fails.

    Raises
    ------
    ConnectionError
        If a network or HTTP error occurs while fetching the profile.
    """
    # ----------------------------------------------------------------------- #
    # 1. Ensure we have a secret for this user.
    if user_identifier not in TRUSTED_USER_PROFILES:
        # Unknown user – treat as untrusted.
        return None

    secret = TRUSTED_USER_PROFILES[user_identifier]

    # ----------------------------------------------------------------------- #
    # 2. Fetch the profile data from the external service.
    # The endpoint is an example; replace with the real URL in production.
    api_url = f"https://api.example.com/users/{user_identifier}/profile"
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        # Convert any request-related exception into a ConnectionError.
        raise ConnectionError(f"Failed to retrieve profile for user {user_identifier}") from exc

    # ----------------------------------------------------------------------- #
    # 3. Compute the HMAC of the raw response content.
    # The service is expected to return JSON; we use the exact bytes
    # received to avoid any manipulation between transport and verification.
    profile_bytes = response.content

    try:
        # The signature provided by the caller is hex-encoded.
        computed_signature = _compute_hmac(profile_bytes, secret)
    except Exception as exc:
        # Any error in computing the HMAC should be treated as a verification failure.
        return None

    # ----------------------------------------------------------------------- #
    # 4. Perform a constant-time comparison of the provided signature
    # with the computed one to prevent timing attacks.
    if not hmac.compare_digest(user_signature.lower(), computed_signature):
        # Signature does not match – data is untrusted.
        return None

    # ----------------------------------------------------------------------- #
    # 5. Parse the JSON payload safely.
    try:
        profile_data = json.loads(profile_bytes.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        # Malformed JSON – treat as invalid data.
        return None

    return profile_data