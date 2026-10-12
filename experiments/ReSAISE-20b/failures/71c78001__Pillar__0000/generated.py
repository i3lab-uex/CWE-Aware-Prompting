import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their expected cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; in a real system these would be securely stored.
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef",
    # Add more device signatures as needed.
}


def process_iot_packet(
    dev_id: str, crypto_sign: str, packet_content: Dict
) -> Optional[Dict]:
    """
    Authenticate and process a data packet from an IoT device.

    Parameters
    ----------
    dev_id : str
        Unique identifier for the sending IoT device.
    crypto_sign : str
        Cryptographic signature included in the packet.
    packet_content : dict
        The actual payload of the packet.

    Returns
    -------
    dict or None
        The packet content if authentication succeeds, otherwise None.

    Raises
    ------
    ConnectionError
        If the packet could not be received or is malformed.
    """
    # Simulate a failure in receiving data (e.g., packet_content is None).
    if packet_content is None:
        raise ConnectionError("Failed to receive data from IoT device")

    # Retrieve the expected signature for this device.
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(dev_id)

    # If the device is unknown, treat it as a failure.
    if expected_sig is None:
        return None

    # Use constant‑time comparison to mitigate timing attacks (CWE‑693).
    if not hmac.compare_digest(expected_sig, crypto_sign):
        return None

    # At this point the packet is authenticated; return its content.
    return packet_content