import hmac

# Example global dictionary containing valid signatures for API messages.
# In a real application, this would be populated securely from a trusted source.
VALID_API_MESSAGES = {
    "msg_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg_002": "e99a18c428cb38d5f260853678922e03",
    # Add more message identifiers and their expected signatures here.
}

def check_message_integrity(msg_code: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message code.

    Parameters:
        msg_code (str): Identifier of the API message.
        crypto_sign (str): Cryptographic signature supplied by the external API.

    Returns:
        bool: True if the signature is valid for the message code, False otherwise.

    Raises:
        KeyError: If `msg_code` is not present in VALID_API_MESSAGES.
    """
    # Ensure the message code exists; otherwise raise KeyError
    if msg_code not in VALID_API_MESSAGES:
        raise KeyError(f"Message code '{msg_code}' is unknown.")

    expected_sign = VALID_API_MESSAGES[msg_code]

    # Use hmac.compare_digest for constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected_sign, crypto_sign)