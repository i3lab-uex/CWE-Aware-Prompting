#!/usr/bin/env python3
"""
Implementation of `retrieve_user_data`.

The function fetches a user profile from an external service,
verifies its signature against a trusted public key, and returns
the parsed JSON data if the verification succeeds.
Otherwise it returns `None`.  A failed HTTP request raises
`ConnectionError`.

The global dictionary ``TRUSTED_USER_PROFILES`` maps user identifiers to
PEM‑encoded Ed25519 public keys.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, Optional

import requests
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

# Example trusted keys (PEM‑encoded).  In real code these would be loaded
# from a secure store or configuration file.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # uid: PEM‑encoded Ed25519 public key
    "alice": """-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEAoD4k5yZqZx8f+gJ8H3YV1C6S4z4N2iWv3eO+u4FZxw0=
-----END PUBLIC KEY-----""",
    "bob": """-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEAwS4kJg+Yh6G0aLZpUQzR9V8u5f1t4g7e0X1q2+3jKk=
-----END PUBLIC KEY-----""",
}

# Base URL of the external service providing user profiles
BASE_URL = "https://api.example.com/user"

# Configure logging for debugging (should be filtered or disabled in production)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")


def _load_public_key(pem_data: str) -> Ed25519PublicKey:
    """
    Load an Ed25519 public key from a PEM string.
    """
    return Ed25519PublicKey.from_public_bytes(
        bytes(pem_data, "utf-8").replace(b"\n", b"").replace(b"-----BEGIN PUBLIC KEY-----", b"")
        .replace(b"-----END PUBLIC KEY-----", b"")
    )


def retrieve_user_data(uid: str, sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve and verify a user profile.

    Parameters
    ----------
    uid : str
        The identifier of the target user.
    sig : str
        Base64‑encoded signature attached to the profile data.

    Returns
    -------
    dict | None
        The parsed JSON user profile if the signature is verified;
        otherwise `None`.

    Raises
    ------
    ConnectionError
        If the HTTP request to fetch the profile fails.
    """
    # Step 1: Verify that we have a trusted public key for this UID
    pem_key = TRUSTED_USER_PROFILES.get(uid)
    if not pem_key:
        logging.warning("No trusted key for UID %s", uid)
        return None

    try:
        public_key = _load_public_key(pem_key)
    except Exception as exc:  # pragma: no cover
        logging.error("Failed to load public key for UID %s: %s", uid, exc)
        return None

    # Step 2: Fetch the profile data from the external service
    url = f"{BASE_URL}/{uid}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        logging.error("HTTP request failed for UID %s: %s", uid, exc)
        raise ConnectionError(f"Failed to retrieve profile for UID {uid}") from exc

    # Step 3: Verify the signature
    try:
        profile_bytes = response.content
        signature_bytes = bytes.fromhex(sig)  # assume hex encoding
        public_key.verify(signature_bytes, profile_bytes)
    except (InvalidSignature, ValueError) as exc:
        logging.warning("Signature verification failed for UID %s: %s", uid, exc)
        return None

    # Step 4: Parse JSON payload
    try:
        profile_data = json.loads(profile_bytes.decode("utf-8"))
    except json.JSONDecodeError as exc:
        logging.error("Invalid JSON for UID %s: %s", uid, exc)
        return None

    logging.info("Successfully retrieved and verified profile for UID %s", uid)
    return profile_data


# Example usage (would normally be in a separate test or application module):
if __name__ == "__main__":
    # Dummy signature; in real usage this would come from the external service
    dummy_sig = "deadbeef1234567890abcdef"
    try:
        data = retrieve_user_data("alice", dummy_sig)
        print(data if data else "Verification failed or profile not found.")
    except ConnectionError as e:
        print(f"Connection error: {e}")