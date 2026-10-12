#!/usr/bin/env python3
"""
Securely fetch a user profile and verify its cryptographic signature.

The module expects a global dictionary `TRUSTED_USER_PROFILES` that maps
profile identifiers to the PEM‑encoded public key used for verifying the
signature of the profile data.

The function `get_user_info` performs the following steps:

1. Retrieves the profile JSON from an external service.
2. Validates that a signature is supplied and corresponds to the data.
3. Returns the parsed profile dictionary on success, otherwise returns
   ``None``.
4. Raises a :class:`ConnectionError` if the HTTP request fails.

The implementation follows best practices to mitigate CWE‑693
(protection mechanism failure) by using a strong cryptographic
verification routine and rejecting any data that fails validation.
"""

import json
import logging
from typing import Any, Dict, Optional

import requests
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# Configure a logger for debugging / audit purposes
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# --------------------------------------------------------------------------- #
# Global mapping of profile IDs to PEM‑encoded RSA public keys
#
# Example structure:
# TRUSTED_USER_PROFILES = {
#     "user123": b"""-----BEGIN PUBLIC KEY-----
# ...PEM data...
# -----END PUBLIC KEY-----""",
#     ...
# }
#
# The dictionary should be populated at application start.
TRUSTED_USER_PROFILES: Dict[str, bytes] = {}


def _load_public_key(pem_data: bytes) -> Any:
    """
    Load an RSA public key from PEM data.

    Parameters
    ----------
    pem_data : bytes
        The PEM‑encoded public key.

    Returns
    -------
    RSAPublicKey
        The loaded RSA public key object.
    """
    return serialization.load_pem_public_key(pem_data)


def _verify_signature(
    public_key: Any, data: bytes, signature: bytes
) -> bool:
    """
    Verify a PKCS#1 v1.5 RSA signature over the given data.

    Parameters
    ----------
    public_key : RSAPublicKey
        The RSA public key used for verification.
    data : bytes
        The original data that was signed.
    signature : bytes
        The signature to verify.

    Returns
    -------
    bool
        ``True`` if the signature is valid, otherwise ``False``.
    """
    try:
        public_key.verify(
            signature,
            data,
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
        return True
    except InvalidSignature:
        logger.warning("Invalid signature for data: %s", data)
        return False
    except Exception as exc:
        # Catch all other cryptographic errors
        logger.error("Signature verification error: %s", exc)
        return False


def get_user_info(profile_id: str, profile_sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service and validate its signature.

    Parameters
    ----------
    profile_id : str
        Identifier of the user whose profile is being fetched.
    profile_sig : str
        Base64‑encoded cryptographic signature of the profile data.

    Returns
    -------
    dict | None
        The parsed JSON profile if verification succeeds; otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the HTTP request to fetch the profile fails.
    """
    # ----------------------------------------------------------------------- #
    # 1. Validate input
    if not profile_id:
        logger.error("Missing profile_id.")
        return None

    # Decode the signature from base64
    try:
        import base64

        sig_bytes = base64.b64decode(profile_sig)
    except Exception as exc:
        logger.error("Failed to decode signature: %s", exc)
        return None

    # ----------------------------------------------------------------------- #
    # 2. Fetch profile data from external service
    url = f"https://api.example.com/profiles/{profile_id}"
    try:
        response = requests.get(url, timeout=5.0)
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.error("Failed to retrieve profile %s: %s", profile_id, exc)
        raise ConnectionError(f"Could not fetch profile {profile_id}") from exc

    # ----------------------------------------------------------------------- #
    # 3. Verify that we have a trusted public key for this profile
    pem_key = TRUSTED_USER_PROFILES.get(profile_id)
    if not pem_key:
        logger.warning("No trusted public key for profile %s", profile_id)
        return None

    try:
        pub_key = _load_public_key(pem_key)
    except Exception as exc:
        logger.error("Failed to load public key for %s: %s", profile_id, exc)
        return None

    # ----------------------------------------------------------------------- #
    # 4. Verify the signature
    profile_bytes = response.content
    if not _verify_signature(pub_key, profile_bytes, sig_bytes):
        logger.warning("Signature verification failed for profile %s", profile_id)
        return None

    # ----------------------------------------------------------------------- #
    # 5. Parse JSON and return
    try:
        profile_data = json.loads(profile_bytes.decode("utf-8"))
    except json.JSONDecodeError as exc:
        logger.error("JSON parsing error for profile %s: %s", profile_id, exc)
        return None

    logger.info("Successfully retrieved and verified profile %s", profile_id)
    return profile_data