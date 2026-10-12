import hmac
from typing import Dict

# Example predefined dictionary of valid signatures.
# In production, this would be securely populated from a trusted source.
VALID_API_MESSAGES: Dict[str, str] = {
    # msg_id : signature
    "msg-001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg-002": "e99a18c428cb38d5f260853678922e03",
    # ... more entries ...
}


def verify_api_message(msg_id: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the one stored
    for the given message ID.

    Parameters
    ----------
    msg_id : str
        The identifier of the API message to verify.
    sign : str
        The cryptographic signature provided with the message.

    Returns
    -------
    bool
        True if the signature matches the stored value, False otherwise.

    Raises
    ------
    KeyError
        If `msg_id` is not present in :data:`VALID_API_MESSAGES`.
    """
    # Ensure the message ID exists; let KeyError propagate if not.
    expected_sig = VALID_API_MESSAGES[msg_id]

    # Use constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(expected_sig, sign)