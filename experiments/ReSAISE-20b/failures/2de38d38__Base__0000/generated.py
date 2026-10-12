import hmac

# Example global dictionary containing valid signatures for API messages.
# In a real application, this would be populated securely from a trusted source.
VALID_API_MESSAGES = {
    "msg001": "5f4dcc3b5aa765d61d8327deb882cf99",  # example SHA-1 hash
    "msg002": "e99a18c428cb38d5f260853678922e03",
    # ... more message-code to signature mappings ...
}

def check_message_integrity(msg_code: str, crypto_sign: str) -> bool:
    """
    Validate that the provided cryptographic signature matches the expected
    signature for the given message code.

    Parameters:
        msg_code (str): Identifier of the API message.
        crypto_sign (str): Cryptographic signature received from the API.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If `msg_code` does not exist in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; KeyError will propagate if not found
    expected_sign = VALID_API_MESSAGES[msg_code]

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sign, crypto_sign)