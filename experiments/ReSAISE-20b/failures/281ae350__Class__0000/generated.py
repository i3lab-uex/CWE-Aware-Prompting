import hmac

# Example global dictionary of valid signatures.
# In a real application this would be securely stored and loaded.
VALID_API_MESSAGES = {
    "msg1": "a1b2c3d4e5f6g7h8i9j0",
    "msg2": "1234567890abcdef1234",
    # Add more message identifiers and their expected signatures here.
}


def validate_api_message(msg_identifier: str, crypto_signature: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the expected
    signature for a given message identifier.

    Parameters
    ----------
    msg_identifier : str
        The unique identifier of the message being validated.
    crypto_signature : str
        The cryptographic signature to validate.

    Returns
    -------
    bool
        True if the signature is valid, False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Ensure the message identifier exists; otherwise raise KeyError
    if msg_identifier not in VALID_API_MESSAGES:
        raise KeyError(f"Unknown message identifier: {msg_identifier}")

    # Retrieve the expected signature
    expected_signature = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_signature, crypto_signature)