import json
from typing import Any, Dict, Optional

import requests
import hmac
import hashlib

# Global dictionary mapping user IDs to their expected HMAC signatures.
# In a real system this would be stored securely (e.g. in a secrets manager).
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries – in practice these would be real HMAC values.
    "alice": "5f2c1e6b7a9d3e8f0c4b5a6d7e8f9a0b1c2d3e4f",
    "bob":   "7e8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6g",
}

# Shared secret key used for HMAC verification.
# In production this should be stored securely and rotated regularly.
_SHARED_SECRET = b"super_secret_key"

def _compute_hmac(data: bytes) -> str:
    """
    Compute a hex-encoded HMAC-SHA256 of the provided data using the shared secret.
    """
    return hmac.new(_SHARED_SECRET, data, hashlib.sha256).hexdigest()


def collect_user_data(user_identifier: str, user_signature: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service and validate its cryptographic signature.

    Args:
        user_identifier: The identifier of the target user.
        user_signature:  The cryptographic signature attached to the profile data.

    Returns:
        The parsed JSON profile if the signature is verified; otherwise None.

    Raises:
        ConnectionError: If the external service cannot be reached or returns a non‑200 status.
    """
    # Step 1: Fetch the profile data from an external API
    url = f"https://api.example.com/users/{user_identifier}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ConnectionError(f"Failed to retrieve profile for {user_identifier}") from exc

    # Parse the JSON payload
    try:
        profile_data = response.json()
    except json.JSONDecodeError as exc:
        raise ConnectionError(f"Invalid JSON returned for {user_identifier}") from exc

    # Step 2: Verify the signature
    # Compute HMAC of the raw response content to ensure integrity.
    computed_sig = _compute_hmac(response.content)

    # Compare using timing‑safe comparison to mitigate side‑channel attacks.
    if not hmac.compare_digest(computed_sig, user_signature):
        # Signature does not match – do not trust the data.
        return None

    # Optional: cross‑check against a pre‑known signature for the user.
    expected_sig = TRUSTED_USER_PROFILES.get(user_identifier)
    if expected_sig and not hmac.compare_digest(computed_sig, expected_sig):
        # The signature does not match the stored trusted value.
        return None

    return profile_data