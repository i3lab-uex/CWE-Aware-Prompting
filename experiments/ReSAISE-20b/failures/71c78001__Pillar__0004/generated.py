import hmac
from typing import Dict, Optional

# Global dictionary mapping device IDs to their expected cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (should be populated with real values in production)
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef",
}


def process_iot_packet(dev_id: str, crypto_sign: str, packet_content: Dict) -> Optional[Dict]:
    """
    Authenticate an IoT data packet and return its content if the signature is valid.

    Parameters
    ----------
    dev_id : str
        Unique identifier of the IoT device.
    crypto_sign : str
        Cryptographic signature attached to the packet.
    packet_content : dict
        The actual payload of the packet.

    Returns
    -------
    dict or None
        The packet content if the signature matches the trusted value; otherwise, None.

    Raises
    ------
    ConnectionError
        If data reception from the device fails (simulated here by an empty packet_content).
    """
    # Simulate a potential data reception issue
    if packet_content is None:
        raise ConnectionError(f"Failed to receive data from device {dev_id}")

    # Retrieve the expected signature for this device
    expected_sign = TRUSTED_DEVICE_SIGNATURES.get(dev_id)

    # If the device is unknown or has no stored signature, reject silently
    if expected_sign is None:
        return None

    # Use constant‑time comparison to mitigate timing attacks (CWE-693)
    if not hmac.compare_digest(expected_sign, crypto_sign):
        return None

    # Signature is valid; return the packet content
    return packet_content