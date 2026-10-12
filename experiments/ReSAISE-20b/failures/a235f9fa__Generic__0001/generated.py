import hmac

# Global dictionary mapping message IDs to their valid signatures.
# In a real application this would be populated from secure storage.
VALID_API_MESSAGES = {
    # Example entries
    "msg_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg_002": "e99a18c428cb38d5f260853678922e03",
    # Add more message IDs and signatures as needed
}


def validate_message(msg_id: str, sig: str) -> bool:
    """
    Validate the cryptographic signature of a message.

    Parameters
    ----------
    msg_id : str
        The identifier for the message whose authenticity needs to be checked.
    sig : str
        The cryptographic signature associated with the specified message.

    Returns
    -------
    bool
        True if the provided signature matches the expected one for the given
        message ID, otherwise False.

    Raises
    ------
    KeyError
        If the `msg_id` does not exist in the VALID_API_MESSAGES dictionary.
    """
    # Retrieve the expected signature. This will raise KeyError if msg_id is missing.
    expected_sig = VALID_API_MESSAGES[msg_id]

    # Use constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected_sig, sig)