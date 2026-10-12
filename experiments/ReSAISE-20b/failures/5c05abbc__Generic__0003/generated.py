import hmac
from typing import Dict

# Predefined global dictionary of valid API message signatures.
# Example: {"msg123": "signature_string", ...}
VALID_API_MESSAGES: Dict[str, str] = {
    # This dictionary should be populated with actual message IDs and their signatures.
}

def verify_api_message(msg_id: str, sign: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a given message ID.

    Parameters:
        msg_id (str): The unique identifier of the API message.
        sign (str): The cryptographic signature received from the external API.

    Returns:
        bool: True if the signatures match, False otherwise.

    Raises:
        KeyError: If `msg_id` is not present in the VALID_API_MESSAGES dictionary.
    """
    # Retrieve the expected signature; raise KeyError if msg_id is missing
    expected_sign = VALID_API_MESSAGES[msg_id]

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(sign, expected_sign)