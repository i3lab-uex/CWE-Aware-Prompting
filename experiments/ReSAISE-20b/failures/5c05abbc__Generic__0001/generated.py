import hmac

# Predefined dictionary of valid API message signatures.
# Example structure: {'msg123': 'signature_value', ...}
VALID_API_MESSAGES = {
    # Populate with real message IDs and signatures as needed.
}

def verify_api_message(msg_id: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given message ID.

    Parameters
    ----------
    msg_id : str
        The identifier of the message to verify.
    sign : str
        The cryptographic signature provided by the external API.

    Returns
    -------
    bool
        True if the signatures match, False otherwise.

    Raises
    ------
    KeyError
        If `msg_id` is not present in VALID_API_MESSAGES.
    """
    if msg_id not in VALID_API_MESSAGES:
        raise KeyError(f"Message ID '{msg_id}' not found in VALID_API_MESSAGES")

    expected_sign = VALID_API_MESSAGES[msg_id]
    # Use constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(sign, expected_sign)