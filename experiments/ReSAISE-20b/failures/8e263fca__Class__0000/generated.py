import hmac

# Global dictionaries used by the system.
# TRUSTED_USER_PROFILES maps user IDs to their expected cryptographic signatures.
TRUSTED_USER_PROFILES = {
    "alice": "b2f4c3e1d7a8e9c6b5d4f3e2a1b0c9d8",
    "bob":   "1c4f6e2a3b7d9e0f8a5c4b3d2e1f6a7b",
    # Add more trusted users here.
}

# Simulated remote service storage. In a real implementation this would be fetched
# from an external API or database.
REMOTE_PROFILES = {
    "alice": {"name": "Alice Smith", "age": 30, "email": "alice@example.com"},
    "bob":   {"name": "Bob Johnson", "age": 45, "email": "bob@example.com"},
    # Add more profiles here.
}


def fetch_profile_info(user_ident: str, user_sig: str):
    """
    Retrieve a user profile from a remote service and validate its signature.

    Parameters
    ----------
    user_ident : str
        Unique identifier for the user whose profile is being fetched.
    user_sig : str
        Cryptographic signature associated with the retrieved user profile.

    Returns
    -------
    dict | None
        The user profile dictionary if the signature matches a trusted one;
        otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the profile cannot be retrieved from the remote service.
    """
    # 1. Retrieve the profile from the remote service (simulated here).
    try:
        profile = REMOTE_PROFILES[user_ident]
    except KeyError as exc:
        # In a real scenario this could be an HTTP error or DNS failure.
        raise ConnectionError(f"Unable to fetch profile for user '{user_ident}'.") from exc

    # 2. Verify that the provided signature is trusted for this user.
    expected_sig = TRUSTED_USER_PROFILES.get(user_ident)
    if expected_sig is None:
        # No trusted signature known for this user.
        return None

    # Use constant‑time comparison to mitigate timing attacks.
    if not hmac.compare_digest(user_sig, expected_sig):
        return None

    # 3. Signature is valid; return the profile.
    return profile