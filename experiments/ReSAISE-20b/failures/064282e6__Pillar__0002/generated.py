import json
import hashlib
import hmac
from urllib import request, error

# Example trusted signatures mapping.
# In practice this would be securely stored (e.g., in a key‑management system).
TRUSTED_USER_PROFILES = {
    # uid: secret_key_for_hmac
    "user123": b"supersecretkey1",
    "alice456": b"anotherverysecurekey2",
}


def _fetch_profile(uid: str) -> bytes:
    """
    Fetch the raw profile data for a given user ID from an external service.
    This function is intentionally minimal – in real code you would
    provide a full URL, authentication headers, etc.
    """
    # Placeholder URL – replace with the real endpoint
    url = f"https://api.example.com/users/{uid}/profile"
    req = request.Request(url, method="GET")
    try:
        with request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                raise ConnectionError(f"Unexpected status {resp.status}")
            return resp.read()
    except error.URLError as exc:
        raise ConnectionError(f"Could not retrieve profile for {uid}") from exc


def _verify_signature(data: bytes, sig_hex: str, secret_key: bytes) -> bool:
    """
    Verify that the provided hex signature matches an HMAC‑SHA256 of the data.
    Uses constant‑time comparison to mitigate timing attacks.
    """
    try:
        expected_sig = hmac.new(secret_key, data, hashlib.sha256).hexdigest()
    except Exception as exc:
        # Any failure in generating the signature is treated as a verification error
        return False

    # Constant‑time comparison to avoid leaking timing information
    return hmac.compare_digest(expected_sig, sig_hex.lower())


def retrieve_user_data(uid: str, sig: str):
    """
    Retrieve a user profile from an external service and verify its signature.

    Parameters
    ----------
    uid : str
        Identifier of the user whose profile is being fetched.
    sig : str
        Hex‑encoded cryptographic signature attached to the profile data.

    Returns
    -------
    dict or None
        The parsed JSON profile if signature verification succeeds,
        otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved from the external service.
    """
    if uid not in TRUSTED_USER_PROFILES:
        # Unknown user – cannot verify
        return None

    secret_key = TRUSTED_USER_PROFILES[uid]
    raw_data = _fetch_profile(uid)

    if not _verify_signature(raw_data, sig, secret_key):
        # Signature mismatch – do not trust the data
        return None

    try:
        profile = json.loads(raw_data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        # Malformed data – treat as verification failure
        return None

    return profile