import hmac

# Global dictionary containing valid signatures for API messages.
# Example structure: {"msg1": "signature_hex_string", ...}
VALID_API_MESSAGES = {
    # Populate with actual message codes and their valid signatures.
}


def check_message_integrity(msg_code: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message code.

    Parameters
    ----------
    msg_code : str
        Identifier of the message to validate.
    crypto_sign : str
        Cryptographic signature received from the external API.

    Returns
    -------
    bool
        True if the signature matches the expected value; False otherwise.

    Raises
    ------
    KeyError
        If `msg_code` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature for the given message code.
    expected_sign = VALID_API_MESSAGES[msg_code]  # Raises KeyError if not found

    # Use constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected_sign, crypto_sign)