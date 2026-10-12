import hmac
from typing import Any, Dict, Optional

# Global mapping of user identifiers to their expected cryptographic signatures.
TRUSTED_USER_PROFILES: Dict[str, str] = {
    "user123": "5f4dcc3b5aa765d61d8327deb882cf99",
    "alice":   "e99a18c428cb38d5f260853678922e03",
    # Add more trusted users and signatures as needed.
}


def _fetch_profile(identifier: str) -> Dict[str, Any]:
    """
    Simulate a network call to retrieve the user profile.

    In a real implementation this would perform an HTTP request or similar
    operation.  For demonstration purposes we simply return a hard‑coded
    dictionary.  If the network is unavailable or any other connectivity issue
    occurs, a ConnectionError will be raised.

    Parameters
    ----------
    identifier : str
        The unique user ID for which to fetch the profile.

    Returns
    -------
    dict
        A dictionary containing user profile information.
    """
    # Simulated network failure scenario:
    if identifier == "offline":
        raise ConnectionError("Unable to reach the remote system.")

    # Simulated user profiles (replace with actual network retrieval).
    simulated_profiles = {
        "user123": {"name": "John Doe", "email": "john@example.com"},
        "alice":   {"name": "Alice Smith", "email": "alice@example.com"},
    }
    profile = simulated_profiles.get(identifier)
    if profile is None:
        raise ConnectionError(f"Profile for '{identifier}' not found on remote system.")
    return profile


def access_user_details(identifier: str, crypt_sig: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from a remote system and verify its authenticity.

    The function fetches the profile data, then verifies that the provided
    cryptographic signature matches the expected one stored in
    ``TRUSTED_USER_PROFILES``.  If the signature is valid, the profile data
    is returned; otherwise ``None`` is returned.  Any connectivity problems
    raise a :class:`ConnectionError`.

    Parameters
    ----------
    identifier : str
        Unique user ID whose profile is to be retrieved.
    crypt_sig : str
        Cryptographic signature accompanying the profile data.

    Returns
    -------
    dict | None
        The user profile if the signature is valid; otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be fetched due to a network or connectivity issue.
    """
    # Basic type validation
    if not isinstance(identifier, str) or not isinstance(crypt_sig, str):
        raise ValueError("Both 'identifier' and 'crypt_sig' must be strings.")

    # Fetch the profile from the remote system
    try:
        profile = _fetch_profile(identifier)
    except ConnectionError as exc:
        # Propagate connectivity errors to the caller
        raise

    # Retrieve the expected signature for this user
    expected_sig = TRUSTED_USER_PROFILES.get(identifier)
    if expected_sig is None:
        # No trusted signature for this user; treat as invalid
        return None

    # Use constant‑time comparison to avoid timing attacks
    if hmac.compare_digest(crypt_sig, expected_sig):
        return profile

    # Signature mismatch
    return None