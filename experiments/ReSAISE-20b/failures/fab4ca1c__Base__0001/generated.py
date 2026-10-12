import hmac

# Global dictionary of valid signatures for API messages.
# Example:
# VALID_API_MESSAGES = {
#     "msg1": "5f4dcc3b5aa765d61d8327deb882cf99",
#     "msg2": "e99a18c428cb38d5f260853678922e03",
#     ...
# }
VALID_API_MESSAGES = {}


def verify_message(msg_identifier: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message identifier.

    Parameters:
        msg_identifier (str): Identifier of the API message.
        sign (str): Cryptographic signature received from the external API.

    Returns:
        bool: True if the signature is valid, False otherwise.

    Raises:
        KeyError: If msg_identifier is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if missing
    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(sign, expected_sign)