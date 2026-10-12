import requests
import hmac
import json

# Example trusted signatures dictionary (user_id -> signature)
TRUSTED_USER_PROFILES = {
    # "uuid": "expected_signature",
}

def collect_user_data(uuid: str, sig_hash: str):
    """
    Fetch a user profile from the remote system and verify its signature.

    Parameters
    ----------
    uuid : str
        Unique identifier of the user.
    sig_hash : str
        Cryptographic signature received with the profile data.

    Returns
    -------
    dict | None
        The user profile as a dictionary if the signature is valid,
        otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to a network or server error.
    """
    # URL endpoint for fetching user profile (placeholder)
    url = f"https://api.example.com/users/{uuid}/profile"

    try:
        # Use a reasonable timeout and verify SSL
        response = requests.get(url, timeout=5.0, verify=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Wrap any request-related error in ConnectionError
        raise ConnectionError(f"Failed to fetch profile for user {uuid}") from exc

    try:
        # Parse JSON payload
        profile = response.json()
    except ValueError as exc:
        # Malformed JSON is treated as a connectivity/format issue
        raise ConnectionError(f"Invalid response format for user {uuid}") from exc

    # Retrieve the expected signature
    expected_sig = TRUSTED_USER_PROFILES.get(uuid)

    if expected_sig is None:
        # No trusted signature known for this user
        return None

    # Constant‑time comparison to mitigate timing attacks (CWE‑693)
    if hmac.compare_digest(sig_hash, expected_sig):
        return profile

    # Signature mismatch
    return None