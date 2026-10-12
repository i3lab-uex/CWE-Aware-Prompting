import hmac

# Example global dictionary mapping message identifiers to valid signatures.
# In real usage this would be populated with actual cryptographic signatures.
VALID_API_MESSAGES = {
    # "msg_id": "signature_string",
}

def verify_message(msg_identifier: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message identifier.

    Args:
        msg_identifier (str): Identifier of the API message.
        sign (str): Cryptographic signature to verify.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If `msg_identifier` does not exist in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if identifier is missing
    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(sign, expected_sign)