import hmac

# Example global dictionary of valid signatures.
# In a real application this would be populated securely (e.g., from a database or environment variables).
VALID_API_MESSAGES = {
    "msg_001": "a1b2c3d4e5f6g7h8i9j0",
    "msg_002": "1234567890abcdef1234",
    # Add more message-id:signature pairs as needed
}


def check_api_signature(api_message: str, sig: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored signature
    for a given API message.

    Parameters
    ----------
    api_message : str
        Unique identifier of the message to validate.
    sig : str
        Cryptographic signature received from the external API.

    Returns
    -------
    bool
        True if the signature matches the stored one, False otherwise.

    Raises
    ------
    KeyError
        If `api_message` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Ensure the message exists; otherwise raise KeyError as required
    if api_message not in VALID_API_MESSAGES:
        raise KeyError(f"Unknown API message identifier: {api_message}")

    expected_sig = VALID_API_MESSAGES[api_message]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(sig, expected_sig)