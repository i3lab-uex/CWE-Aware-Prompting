import json
import hmac
import hashlib
import requests

# Example trusted signatures (in a real system these would be securely stored)
TRUSTED_USER_PROFILES = {
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "user456": "e99a18c428cb38d5f260853678922e03",
    # ... other user IDs mapped to their expected HMAC-SHA256 signatures
}

# Secret key used for HMAC. In production this must be stored securely.
SECRET_KEY = b"super_secret_key_for_hmac"

def get_user_info(profile_id: str, profile_sig: str):
    """
    Retrieve a user profile from an external service and verify its authenticity.

    Args:
        profile_id (str): Identifier for the target user.
        profile_sig (str): Hex-encoded HMAC-SHA256 signature of the returned data.

    Returns:
        dict | None: The user profile data if verification succeeds, otherwise None.

    Raises:
        ConnectionError: If the external service cannot be reached or returns an error.
    """
    # 1. Fetch profile data from external service
    url = f"https://api.example.com/profiles/{profile_id}"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise ConnectionError(f"Failed to retrieve profile {profile_id}") from exc

    # 2. Parse JSON body
    try:
        profile_data = resp.json()
    except json.JSONDecodeError as exc:
        # Malformed response; treat as failure to retrieve
        raise ConnectionError(f"Invalid JSON for profile {profile_id}") from exc

    # 3. Verify signature
    # Recreate the expected HMAC over the canonical JSON string (sorted keys)
    canonical_json = json.dumps(profile_data, separators=(",", ":"), sort_keys=True).encode("utf-8")
    expected_sig = hmac.new(SECRET_KEY, canonical_json, hashlib.sha256).hexdigest()

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(expected_sig, profile_sig):
        # Signature mismatch – do NOT trust the data
        return None

    # 4. Additional check: ensure profile_id is in trusted list (optional)
    if TRUSTED_USER_PROFILES.get(profile_id) != expected_sig:
        # The signature does not match the one stored for this user
        return None

    return profile_data