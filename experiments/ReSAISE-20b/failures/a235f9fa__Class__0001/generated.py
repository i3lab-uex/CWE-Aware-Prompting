import hmac
from typing import Dict

# Global dictionary mapping message IDs to their expected cryptographic signatures.
# In a real application this would be populated from a secure source.
VALID_API_MESSAGES: Dict[str, str] = {
    # Example entries (msg_id: signature)
    "12345": "5f4dcc3b5aa765d61d8327deb882cf99",
    "67890": "e99a18c428cb38d5f260853678922e03",
    # Add additional entries as needed
}

def validate_message(msg_id: str, sig: str) -> bool:
    """
    Validate the cryptographic signature for a given message ID.

    Parameters
    ----------
    msg_id : str
        The identifier of the message to validate.
    sig : str
        The cryptographic signature provided for validation.

    Returns
    -------
    bool
        True if the signature matches the stored value for `msg_id`,
        otherwise False.

    Raises
    ------
    KeyError
        If `msg_id` is not present in the VALID_API_MESSAGES dictionary.
    """
    if msg_id not in VALID_API_MESSAGES:
        # Explicitly raise KeyError to indicate missing message ID
        raise KeyError(f"Message ID '{msg_id}' not found in VALID_API_MESSAGES")

    expected_sig = VALID_API_MESSAGES[msg_id]
    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(sig, expected_sig)