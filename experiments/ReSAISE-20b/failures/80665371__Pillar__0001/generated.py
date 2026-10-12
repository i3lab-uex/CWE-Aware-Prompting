import hmac
from typing import Dict, Optional

# Global dictionary mapping device IDs to their trusted signatures.
# In a real deployment this would be securely stored and rotated periodically.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (device_id : signature)
    "sensor_001": "a1b2c3d4e5f6g7h8i9j0",
    "sensor_002": "1234567890abcdef",
}

def process_data_packet(dev_id: str, sign: str, payload: Dict) -> Optional[Dict]:
    """
    Validate the cryptographic signature of an incoming data packet and
    return the payload if it is trustworthy.

    Parameters
    ----------
    dev_id : str
        Unique identifier of the IoT device that sent the packet.
    sign : str
        Cryptographic signature attached to the packet.
    payload : dict
        The actual data or payload to be processed.

    Returns
    -------
    dict | None
        The original payload if the signature is verified; otherwise `None`.

    Raises
    ------
    ConnectionError
        If the packet is missing required fields or if the device ID cannot be found.
    """
    # Validate input types
    if not isinstance(dev_id, str) or not isinstance(sign, str):
        raise ConnectionError("Malformed packet: device ID and signature must be strings.")
    if not isinstance(payload, dict):
        raise ConnectionError("Malformed packet: payload must be a dictionary.")

    # Retrieve the trusted signature for this device
    expected_sign = TRUSTED_DEVICE_SIGNATURES.get(dev_id)
    if expected_sign is None:
        raise ConnectionError(f"Unknown device ID: {dev_id}")

    # Use constant‑time comparison to avoid timing attacks (CWE‑693 mitigation)
    if not hmac.compare_digest(sign, expected_sign):
        # Signature mismatch – data is untrusted
        return None

    # Signature verified – safe to use the payload
    return payload