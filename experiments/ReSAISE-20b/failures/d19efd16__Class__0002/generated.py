import json
import hmac
import hashlib
import requests
from typing import Optional

# Global dictionary that maps user IDs to the expected cryptographic signatures
TRUSTED_USER_PROFILES = {
    # Example entries: user_id -> expected signature (hex string)
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "user456": "e99a18c428cb38d5f260853678922e03",
    # Add more entries as needed
}

def get_user_info(profile_id: str, profile_sig: str) -> Optional[dict]:
    """
    Retrieve a user profile from an external service and verify its signature.

    Parameters
    ----------
    profile_id : str
        Identifier for the user whose profile is being fetched.
    profile_sig : str
        Cryptographic signature attached to the profile data (hex string).

    Returns
    -------
    dict or None
        The user profile dictionary if the signature is verified successfully,
        otherwise None.

    Raises
    ------
    ConnectionError
        If the HTTP request to retrieve the profile fails.
    """
    # ------------------------------------------------------------------
    # 1. Retrieve the expected signature from TRUSTED_USER_PROFILES
    # ------------------------------------------------------------------
    expected_sig = TRUSTED_USER_PROFILES.get(profile_id)
    if not expected_sig:
        # No known signature for this profile; treat as untrusted
        return None

    # ------------------------------------------------------------------
    # 2. Validate the signature format (must be a valid hex string)
    # ------------------------------------------------------------------
    try:
        bytes.fromhex(profile_sig)
    except ValueError:
        return None  # Invalid signature format

    try:
        bytes.fromhex(expected_sig)
    except ValueError:
        # Corrupted trusted data – treat as untrusted
        return None

    # ------------------------------------------------------------------
    # 3. Fetch the profile data from an external service
    # ------------------------------------------------------------------
    try:
        response = requests.get(
            f"https://api.example.com/profiles/{profile_id}",
            timeout=5,
        )
    except requests.RequestException as exc:
        raise ConnectionError(f"Failed to retrieve profile: {exc}") from exc

    if response.status_code != 200:
        raise ConnectionError(
            f"Unexpected status code {response.status_code} for profile {profile_id}"
        )

    # ------------------------------------------------------------------
    # 4. Compute the hash of the received payload
    # ------------------------------------------------------------------
    payload_bytes = response.content  # raw bytes for accurate hashing

    computed_hash_hex = hashlib.sha256(payload_bytes).hexdigest()

    # ------------------------------------------------------------------
    # 5. Perform a constant‑time comparison of the computed hash with
    #    the expected signature.
    # ------------------------------------------------------------------
    if not hmac.compare_digest(computed_hash_hex, expected_sig):
        return None  # Signature mismatch

    # ------------------------------------------------------------------
    # 6. Parse and return the JSON payload
    # ------------------------------------------------------------------
    try:
        profile_data = json.loads(payload_bytes)
    except json.JSONDecodeError:
        return None  # Malformed JSON – treat as untrusted

    return profile_data