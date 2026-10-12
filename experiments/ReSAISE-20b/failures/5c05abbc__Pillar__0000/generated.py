import hmac
from typing import Dict

# Example of a global dictionary containing valid signatures.
# In practice, this would be populated from a secure source.
VALID_API_MESSAGES: Dict[str, str] = {
    # msg_id : signature
    "msg001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "msg002": "e99a18c428cb38d5f260853678922e03",
    # ... other entries
}


def verify_api_message(msg_id: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    value for a given message ID.

    Parameters:
        msg_id (str): The identifier of the API message.
        sign (str): The cryptographic signature supplied with the message.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        KeyError: If `msg_id` is not present in VALID_API_MESSAGES.
    """
    if msg_id not in VALID_API_MESSAGES:
        # Explicitly raise KeyError to signal missing message ID
        raise KeyError(f"Message ID '{msg_id}' not found in VALID_API_MESSAGES")

    # Retrieve the expected signature
    expected_sign = VALID_API_MESSAGES[msg_id]

    # Use constant‑time comparison to mitigate timing attacks (CWE-693)
    return hmac.compare_digest(expected_sign, sign)