import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (replace with real signatures in production)
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef1234",
}

def process_iot_packet(dev_id: str, crypto_sign: str, packet_content: Dict) -> Optional[Dict]:
    """
    Authenticate an IoT data packet and return its content if the signature is valid.

    Parameters
    ----------
    dev_id : str
        Unique identifier of the sending IoT device.
    crypto_sign : str
        Cryptographic signature attached to the packet.
    packet_content : dict
        The actual payload of the data packet.

    Returns
    -------
    dict | None
        Returns the packet content if authentication succeeds, otherwise None.

    Raises
    ------
    ConnectionError
        If the packet content is missing or not a dictionary, indicating an issue receiving data.
    """
    # Basic sanity checks for the received packet
    if not isinstance(packet_content, dict):
        raise ConnectionError("Invalid or missing packet content received from device.")

    # Retrieve the trusted signature for this device
    expected_sign = TRUSTED_DEVICE_SIGNATURES.get(dev_id)
    if expected_sign is None:
        # Unknown device – treat as authentication failure
        return None

    # Use constant‑time comparison to mitigate timing attacks
    if hmac.compare_digest(expected_sign, crypto_sign):
        return packet_content

    # Signature mismatch – reject the packet
    return None