import hmac

# Global dictionary mapping API messages to their expected cryptographic signatures.
# Example:
# VALID_API_MESSAGES = {
#     "msg1": "a3f5e8c2...",
#     "msg2": "b7d9e1a4..."
# }
VALID_API_MESSAGES = {}


def check_api_signature(api_message: str, sig: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given API message.

    Parameters:
        api_message (str): Identifier of the API message to validate.
        sig (str): Signature supplied by the external source.

    Returns:
        bool: True if the signature is valid for the message, False otherwise.

    Raises:
        KeyError: If `api_message` is not present in VALID_API_MESSAGES.
    """
    if api_message not in VALID_API_MESSAGES:
        raise KeyError(f"Unknown API message: {api_message}")

    expected_sig = VALID_API_MESSAGES[api_message]
    # Use constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(sig, expected_sig)