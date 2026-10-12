import hmac

# Global dictionary containing valid signatures for API messages.
# Example structure:
# VALID_API_MESSAGES = {
#     "msg1": "signature_hex_string_1",
#     "msg2": "signature_hex_string_2",
# }
VALID_API_MESSAGES = {}


def verify_message(msg_identifier: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message identifier.

    Parameters
    ----------
    msg_identifier : str
        Identifier of the API message to validate.
    sign : str
        Signature received from the external API.

    Returns
    -------
    bool
        True if the signature matches the expected value, False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Retrieve expected signature; KeyError propagates if missing
    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(sign, expected_sign)