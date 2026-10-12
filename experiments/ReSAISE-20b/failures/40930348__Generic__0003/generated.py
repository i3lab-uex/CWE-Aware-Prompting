import json
import hmac
import hashlib
from typing import Any, Dict

import requests

# Global mapping of user IDs to their shared secret keys (used for HMAC verification)
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (user_id : secret_key)
    "alice": b"super_secret_alice_key",
    "bob":   b"super_secret_bob_key",
}


def _fetch_profile(user_identifier: str) -> bytes:
    """
    Retrieve the raw profile payload for a user from an external service.

    The function performs an HTTP GET request to a predefined endpoint.
    If the response status is not 200, a ConnectionError is raised.

    Args:
        user_identifier: Identifier of the target user.

    Returns:
        Raw bytes containing the profile payload (JSON encoded).
    """
    # Example endpoint – replace with real service URL
    url = f"https://api.example.com/users/{user_identifier}/profile"

    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise ConnectionError(f"Failed to fetch profile for {user_identifier}") from exc

    return resp.content


def _verify_signature(payload: bytes, signature_hex: str, secret_key: bytes) -> bool:
    """
    Verify that the provided hexadecimal signature matches an HMAC-SHA256
    of the payload using the supplied secret key.

    Args:
        payload: The raw profile data as bytes.
        signature_hex: Signature provided by the caller, hex encoded.
        secret_key: Secret key for HMAC calculation.

    Returns:
        True if the signature is valid, False otherwise.
    """
    # Compute HMAC-SHA256 over the payload
    computed = hmac.new(secret_key, payload, hashlib.sha256).hexdigest()

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(computed, signature_hex)


def collect_user_data(user_identifier: str, user_signature: str) -> Any | None:
    """
    Retrieve a signed user profile from an external service and validate its
    authenticity before returning the parsed data.

    The function fetches the raw profile payload, verifies its signature
    against a shared secret stored in TRUSTED_USER_PROFILES, and returns the
    decoded JSON content if validation succeeds. If verification fails,
    None is returned.

    Args:
        user_identifier: Identifier of the target user.
        user_signature: Cryptographic signature (hex string) attached to
                         the profile data.

    Returns:
        The parsed user profile data (as a Python object) on success,
        otherwise None.

    Raises:
        ConnectionError: If the profile cannot be retrieved from the
                         external service.
    """
    # Step 1: Fetch raw profile data
    payload = _fetch_profile(user_identifier)

    # Step 2: Retrieve the shared secret key for this user
    secret_key = TRUSTED_USER_PROFILES.get(user_identifier)
    if secret_key is None:
        # Unknown user – treat as untrusted
        return None

    # Step 3: Verify signature
    if not _verify_signature(payload, user_signature, secret_key):
        return None

    # Step 4: Parse JSON payload
    try:
        profile_data = json.loads(payload.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        # Malformed payload – do not trust
        return None

    return profile_data