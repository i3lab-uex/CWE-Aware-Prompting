import hmac

# Example dictionary of expected signatures for each message identifier.
# In a real application this would be populated from secure storage or
# configuration and kept out of source code.
VALID_API_MESSAGES = {
    # "msg_identifier": "expected_signature",
    # e.g., "order_12345": "a1b2c3d4e5f6...",
}

def validate_api_message(msg_identifier: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message identifier.

    Parameters
    ----------
    msg_identifier : str
        Unique identifier of the API message being validated.
    crypto_signature : str
        The cryptographic signature received from the external API.

    Returns
    -------
    bool
        True if the signatures match; False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Ensure the identifier exists
    if msg_identifier not in VALID_API_MESSAGES:
        raise KeyError(f"Unknown message identifier: {msg_identifier}")

    expected_signature = VALID_API_MESSAGES[msg_identifier]

    # Use constant-time comparison to mitigate timing attacks (CWE-347)
    return hmac.compare_digest(crypto_signature, expected_signature)