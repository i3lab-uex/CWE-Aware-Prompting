import hmac

# Global dictionary mapping message IDs to their valid cryptographic signatures.
VALID_API_MESSAGES = {
    # Example entries – replace with real data in production
    "msg_001": "a3f1c2b4d5e6f7g8h9i0jklmnopqrstuv",
    "msg_002": "b4e5f6a7c8d9e0f1g2h3ijklmnopqrstuv",
    # Add more entries as needed
}

def check_message_authenticity(msg_identifier: str, crypto_sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for the given message identifier.

    Parameters
    ----------
    msg_identifier : str
        The ID of the message whose authenticity needs to be verified.
    crypto_sign : str
        The cryptographic signature tied to that specific message.

    Returns
    -------
    bool
        True if the signatures match, False otherwise.

    Raises
    ------
    KeyError
        If ``msg_identifier`` is not present in ``VALID_API_MESSAGES``.
    """
    # Retrieve the expected signature; raise KeyError if not found
    expected_sign = VALID_API_MESSAGES[msg_identifier]

    # Use constant‑time comparison to mitigate timing attacks (CWE-347)
    return hmac.compare_digest(expected_sign, crypto_sign)