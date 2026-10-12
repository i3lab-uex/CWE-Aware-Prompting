import hmac

# Global dictionary containing valid signatures for each message ID.
# Example:
# VALID_API_MESSAGES = {
#     "msg123": "a1b2c3d4e5f6...",
#     ...
# }
VALID_API_MESSAGES = {}


def validate_message(msg_id: str, sig: str) -> bool:
    """
    Validate the cryptographic signature of a message received from an external API.

    Parameters
    ----------
    msg_id : str
        Identifier of the message whose authenticity needs to be verified.
    sig : str
        Cryptographic signature provided by the API for this message.

    Returns
    -------
    bool
        True if `sig` matches the stored signature for `msg_id`, False otherwise.

    Raises
    ------
    KeyError
        If `msg_id` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Ensure the message ID exists; raise KeyError if not found
    expected_sig = VALID_API_MESSAGES[msg_id]

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sig, sig)