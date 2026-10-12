import json
import hmac
import hashlib
from urllib.parse import urljoin, quote
import requests

# Example trusted signatures mapping.
# In a real system these would be securely stored and retrieved.
TRUSTED_USER_PROFILES = {
    # user_id: shared_secret
    "alice": b"supersecretkey1",
    "bob": b"anothersecurekey2",
}


def get_user_info(profile_id: str, profile_sig: str) -> dict | None:
    """
    Retrieve a user profile from an external service and verify its signature.

    Args:
        profile_id (str): Identifier of the user whose profile is requested.
        profile_sig (str): Hex-encoded cryptographic signature of the payload.

    Returns:
        dict | None: The profile data if verification succeeds; otherwise None.

    Raises:
        ConnectionError: If the HTTP request fails or times out.
    """
    # Build a safe URL for the profile endpoint
    base_url = "https://example.com/profiles/"
    # Quote the profile_id to avoid path traversal or injection
    safe_profile_id = quote(profile_id, safe="")
    url = urljoin(base_url, safe_profile_id)

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        raise ConnectionError(f"Failed to retrieve profile for '{profile_id}'.") from exc

    # Ensure we have a byte payload for signature verification
    raw_payload = response.content

    # Retrieve the shared secret for this user
    shared_secret = TRUSTED_USER_PROFILES.get(profile_id)
    if shared_secret is None:
        # No trusted secret; cannot verify authenticity
        return None

    # Compute HMAC-SHA256 over the raw payload
    computed_sig = hmac.new(
        shared_secret, raw_payload, hashlib.sha256
    ).hexdigest()

    # Constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(computed_sig, profile_sig):
        return None

    # Parse JSON safely
    try:
        data = json.loads(raw_payload.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        # Malformed payload; treat as verification failure
        return None

    return data