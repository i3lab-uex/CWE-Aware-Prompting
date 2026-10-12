import hmac

# Global dictionary containing the expected signatures for each message identifier.
# Example:
# VALID_API_MESSAGES = {
#     "msg123": "a1b2c3d4e5f6... (hex or base64 encoded signature)",
#     "msg456": "deadbeefcafebabe..."
# }
VALID_API_MESSAGES = {}


def validate_api_message(msg_identifier: str, crypto_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given message identifier.

    Parameters
    ----------
    msg_identifier : str
        Unique identifier of the API message to validate.
    crypto_signature : str
        Cryptographic signature received from the external API.

    Returns
    -------
    bool
        True if the signature matches the stored value, False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in the VALID_API_MESSAGES dictionary.
    """
    if msg_identifier not in VALID_API_MESSAGES:
        raise KeyError(f"Message identifier '{msg_identifier}' is unknown.")

    expected_signature = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected_signature, crypto_signature)