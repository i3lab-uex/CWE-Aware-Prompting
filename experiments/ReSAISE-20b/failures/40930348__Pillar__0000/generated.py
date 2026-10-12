import json
import hmac
import hashlib
from typing import Any, Dict, Optional

import requests

# Global dictionary mapping user IDs to the expected HMAC signature
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # Example entries (user_id : HMAC-SHA256 signature in hex)
    "alice": "a3f5c1d4e2b7...",
    "bob":   "9f8a6b3c1d0e..."
}

# Shared secret key used for HMAC generation (in a real system this
# should be stored securely, e.g. in an HSM or environment variable)
HMAC_SECRET_KEY = b"super-secret-key"

def collect_user_data(user_identifier: str, user_signature: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from an external service and verify its
    cryptographic signature.

    Args:
        user_identifier: Identifier of the target user.
        user_signature:  Signature attached to the profile data.

    Returns:
        The parsed JSON profile if verification succeeds; otherwise None.

    Raises:
        ConnectionError: If the external service cannot be reached or
                          returns a non-200 status code.
    """
    # 1. Build the request URL (example endpoint)
    url = f"https://api.example.com/users/{user_identifier}/profile"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        raise ConnectionError(f"Failed to retrieve profile for {user_identifier}") from exc

    # 2. Parse the JSON payload
    try:
        profile_data = response.json()
    except ValueError as exc:
        # Malformed JSON
        raise ConnectionError(f"Invalid JSON received for {user_identifier}") from exc

    # 3. Compute the expected HMAC over the canonical JSON representation
    #    (sorted keys to avoid order variations)
    canonical_json = json.dumps(profile_data, separators=(",", ":"), sort_keys=True).encode("utf-8")
    expected_hmac = hmac.new(HMAC_SECRET_KEY, canonical_json, hashlib.sha256).hexdigest()

    # 4. Verify the signature supplied by the caller matches the expected HMAC
    if not hmac.compare_digest(user_signature, expected_hmac):
        # Signature mismatch – do not trust the data
        return None

    # 5. Verify that the signature stored in TRUSTED_USER_PROFILES matches
    trusted_signature = TRUSTED_USER_PROFILES.get(user_identifier)
    if not trusted_signature or not hmac.compare_digest(trusted_signature, expected_hmac):
        # The profile is not trusted for this user
        return None

    # 6. All checks passed – return the profile data
    return profile_data