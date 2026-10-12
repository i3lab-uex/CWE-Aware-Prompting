import hmac
from typing import Dict

# Example global dictionary of expected signatures.
# In a real scenario this would be securely populated and stored.
VALID_API_MESSAGES: Dict[str, str] = {
    # message_id : expected_signature
    "msg_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg_002": "e99a18c428cb38d5f260853678922e03",
    # ... more entries
}


def authenticate_message(message_id: str, signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message_id.

    Parameters
    ----------
    message_id : str
        Unique identifier of the message to be authenticated.
    signature : str
        Cryptographic signature supplied by the external API.

    Returns
    -------
    bool
        True if the signatures match, False otherwise.

    Raises
    ------
    KeyError
        If message_id is not present in VALID_API_MESSAGES.
    """
    # Ensure the message_id exists; let KeyError propagate if not found
    expected_signature = VALID_API_MESSAGES[message_id]

    # Use constant-time comparison to mitigate timing attacks
    return hmac.compare_digest(signature, expected_signature)