#!/usr/bin/env python3
"""
Utility to fetch and verify user profile data from an external service.
"""

import json
import hmac
import hashlib
from typing import Optional, Dict

import requests

# --------------------------------------------------------------------------- #
# Global dictionary containing the shared secrets used to sign user profiles.
# In a real system these would be securely stored and rotated as needed.
TRUSTED_USER_PROFILES: Dict[str, bytes] = {
    # profile_id : secret key (bytes)
    "alice": b"super_secret_key_alice",
    "bob":   b"another_super_secret_key_bob",
}

# Base URL of the external profile service
PROFILE_SERVICE_URL = "https://profiles.example.com/api/v1/user"


def _verify_signature(profile_data: bytes, expected_sig_hex: str, secret_key: bytes) -> bool:
    """
    Verify that the provided signature matches the HMAC-SHA256 of profile_data
    using the given secret key.

    Args:
        profile_data: Raw bytes of the profile payload.
        expected_sig_hex: Hexadecimal string representation of the signature.
        secret_key: Secret key used to compute HMAC.

    Returns:
        True if signatures match, False otherwise.
    """
    # Compute HMAC-SHA256
    mac = hmac.new(secret_key, profile_data, hashlib.sha256)
    # Convert to hex string for comparison
    computed_sig_hex = mac.hexdigest()
    # Constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(computed_sig_hex, expected_sig_hex.lower())


def get_user_info(profile_id: str, profile_sig: str) -> Optional[Dict]:
    """
    Retrieve a user profile from the external service and verify its signature.

    Args:
        profile_id: Identifier of the user whose profile is requested.
        profile_sig: Hexadecimal cryptographic signature attached to the profile data.

    Returns:
        The parsed JSON profile dictionary if verification succeeds, otherwise None.

    Raises:
        ConnectionError: If the HTTP request to the profile service fails.
    """
    # Ensure we have a secret key for this profile
    if profile_id not in TRUSTED_USER_PROFILES:
        raise ValueError(f"Unknown profile ID: {profile_id}")

    secret_key = TRUSTED_USER_PROFILES[profile_id]

    # Construct the request URL
    url = f"{PROFILE_SERVICE_URL}/{profile_id}"
    try:
        # Use a reasonable timeout and verify TLS certificate
        response = requests.get(url, timeout=5.0, verify=True)
        response.raise_for_status()
    except requests.RequestException as exc:
        # Wrap any network-related error into ConnectionError
        raise ConnectionError(f"Failed to retrieve profile for '{profile_id}': {exc}") from exc

    # Raw payload used for signature verification
    raw_payload = response.content

    # Verify the provided signature matches the payload
    if not _verify_signature(raw_payload, profile_sig, secret_key):
        # Signature mismatch – do not trust the data
        return None

    try:
        profile_json = response.json()
    except json.JSONDecodeError:
        # Malformed JSON – treat as verification failure
        return None

    return profile_json


# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Dummy example – replace with real IDs and signatures
    test_id = "alice"
    try:
        # Simulate fetching profile to get a signature (in real life this would come from elsewhere)
        dummy_sig = "deadbeef"  # placeholder
        profile = get_user_info(test_id, dummy_sig)
        if profile:
            print(f"Profile for {test_id}: {profile}")
        else:
            print("Signature verification failed.")
    except Exception as e:
        print(f"Error: {e}")