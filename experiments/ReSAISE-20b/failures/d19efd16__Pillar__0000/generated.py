import json
import hmac
import hashlib
from typing import Optional, Dict

# External dependencies
try:
    import requests  # pip install requests
except ImportError as exc:          # pragma: no cover - defensive import
    raise RuntimeError("The 'requests' library is required.") from exc

# --------------------------------------------------------------------------- #
# Configuration & Global Data
# --------------------------------------------------------------------------- #

# Simulated trusted signatures database. In a real system this would be
# stored in a secure vault or retrieved from a signed manifest.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    # user_id : HMAC signature (hex digest)
    "user123": "5f2c9d1b6e8a4b7d3f0c1e5a2b9d7f6c8e4b1a3d0e2f7c6b9a5d4c3b2e1f8a0",
    # add more entries as needed
}

# Shared secret key for HMAC verification. In practice, this must be stored
# securely (e.g., environment variable, key management service).
SECRET_KEY = b"super-secret-key-that-should-be-long-and-random"

# --------------------------------------------------------------------------- #
# Helper Functions
# --------------------------------------------------------------------------- #

def _compute_hmac(message: bytes) -> str:
    """
    Compute the HMAC-SHA256 hex digest of *message* using the global SECRET_KEY.
    """
    mac = hmac.new(SECRET_KEY, message, hashlib.sha256)
    return mac.hexdigest()

def _verify_signature(profile_id: str, profile_data: dict, signature_hex: str) -> bool:
    """
    Verify that the provided *signature_hex* matches the HMAC of
    the JSON-encoded *profile_data* for *profile_id*.
    """
    # Ensure signature is in the trusted list
    expected_sig = TRUSTED_USER_PROFILES.get(profile_id)
    if not expected_sig:
        return False

    # Recompute HMAC on canonical JSON representation
    json_bytes = json.dumps(profile_data, sort_keys=True).encode("utf-8")
    computed_sig = _compute_hmac(json_bytes)

    # Use hmac.compare_digest to prevent timing attacks
    return hmac.compare_digest(computed_sig, signature_hex) and \
           hmac.compare_digest(expected_sig, signature_hex)

# --------------------------------------------------------------------------- #
# Main Function
# --------------------------------------------------------------------------- #

def get_user_info(profile_id: str, profile_sig: str) -> Optional[dict]:
    """
    Retrieve a user profile from an external service and validate its signature.

    Parameters
    ----------
    profile_id : str
        Identifier for the user whose profile is being fetched.
    profile_sig : str
        Cryptographic signature (hex digest) attached to the profile data.

    Returns
    -------
    dict or None
        The user profile data if signature verification succeeds, otherwise `None`.

    Raises
    ------
    ConnectionError
        If the external service cannot be reached or returns a non‑200 status code.
    """
    # URL construction – in real life this would be configurable
    url = f"https://api.example.com/users/{profile_id}/profile"

    try:
        response = requests.get(url, timeout=5.0)
    except (requests.RequestException, OSError) as exc:
        # Wrap low‑level networking errors in a ConnectionError
        raise ConnectionError(f"Failed to fetch profile for '{profile_id}'.") from exc

    if response.status_code != 200:
        raise ConnectionError(
            f"Unexpected status code {response.status_code} for profile '{profile_id}'."
        )

    try:
        profile_data = response.json()
    except json.JSONDecodeError as exc:          # pragma: no cover
        raise ValueError(f"Invalid JSON received for profile '{profile_id}'.") from exc

    # Verify signature
    if _verify_signature(profile_id, profile_data, profile_sig):
        return profile_data

    # Signature mismatch – do not trust the data
    return None