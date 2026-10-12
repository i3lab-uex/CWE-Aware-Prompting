import hmac

# Global dictionary mapping API message identifiers to their expected signatures.
# Example:
# VALID_API_MESSAGES = {
#     "msg123": "5f2d3e9b1c4a... (hex signature)",
#     ...
# }
VALID_API_MESSAGES = {}

def check_api_signature(api_message: str, sig: str) -> bool:
    """
    Verify that the provided cryptographic signature `sig` matches the expected
    signature stored in VALID_API_MESSAGES for the given `api_message`.

    Parameters
    ----------
    api_message : str
        The unique identifier for the API message being validated.
    sig : str
        The cryptographic signature to validate.

    Returns
    -------
    bool
        True if the signature matches the stored value; False otherwise.

    Raises
    ------
    KeyError
        If `api_message` is not present in VALID_API_MESSAGES.
    """
    # Retrieve the expected signature; raise KeyError if missing
    expected_sig = VALID_API_MESSAGES[api_message]

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(sig, expected_sig)