import hmac

# Predefined global dictionary mapping message IDs to their correct signatures.
VALID_API_MESSAGES = {
    # Example entries; replace with actual data as needed
    "msg001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg002": "e99a18c428cb38d5f260853678922e03",
    # ...
}


def check_message_authenticity(msg_identifier: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    value for a given message identifier.

    Parameters
    ----------
    msg_identifier : str
        The ID of the message to verify.
    crypto_sign : str
        The cryptographic signature supplied by the external API.

    Returns
    -------
    bool
        True if the signatures match, False otherwise.

    Raises
    ------
    KeyError
        If `msg_identifier` is not present in VALID_API_MESSAGES.
    """
    if msg_identifier not in VALID_API_MESSAGES:
        raise KeyError(f"Message identifier '{msg_identifier}' not found.")

    # Use constant‑time comparison to mitigate timing attacks
    expected_sign = VALID_API_MESSAGES[msg_identifier]
    return hmac.compare_digest(expected_sign, crypto_sign)