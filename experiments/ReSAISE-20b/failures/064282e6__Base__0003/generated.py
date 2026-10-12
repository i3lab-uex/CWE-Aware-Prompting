import json
import hmac
import hashlib
from urllib import request, error

# Global mapping of user IDs to the shared secret used for HMAC verification
TRUSTED_USER_PROFILES = {
    # uid: shared_secret (bytes)
    "alice": b"supersecretkey_alice",
    "bob":   b"supersecretkey_bob",
    # Add more trusted users here
}

def retrieve_user_data(uid: str, sig: str):
    """
    Retrieve a user profile from an external service and verify its HMAC signature.

    Parameters
    ----------
    uid : str
        Identifier of the target user.
    sig : str
        Base64‑encoded HMAC signature attached to the profile data.

    Returns
    -------
    dict | None
        The user profile dictionary if the signature is valid; otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the HTTP request to fetch the profile fails.
    """
    # Validate that we have a trusted secret for this user
    shared_secret = TRUSTED_USER_PROFILES.get(uid)
    if not shared_secret:
        # No trusted secret known for this user – reject immediately
        return None

    # Build the URL to fetch the profile.  In a real system this would be
    # configurable or discovered via service discovery.
    url = f"https://example.com/api/users/{uid}/profile"

    try:
        with request.urlopen(url, timeout=10) as resp:
            if resp.status != 200:
                raise ConnectionError(f"Failed to fetch profile: HTTP {resp.status}")
            raw = resp.read()
    except error.URLError as exc:
        raise ConnectionError(f"Network error when retrieving profile: {exc}") from exc

    # Parse the JSON payload
    try:
        data = json.loads(raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        # Malformed JSON – treat as a verification failure
        return None

    # The profile data that was signed is the raw JSON string of the 'profile' field.
    profile_json = json.dumps(data.get("profile", {}), separators=(",", ":"), sort_keys=True).encode("utf-8")

    # Decode the signature from base64
    try:
        import base64
        sig_bytes = base64.b64decode(sig)
    except (base64.binascii.Error, TypeError):
        return None

    # Compute the expected HMAC
    expected = hmac.new(shared_secret, profile_json, hashlib.sha256).digest()

    # Constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(expected, sig_bytes):
        return None

    # Signature verified – return the profile data
    return data.get("profile")