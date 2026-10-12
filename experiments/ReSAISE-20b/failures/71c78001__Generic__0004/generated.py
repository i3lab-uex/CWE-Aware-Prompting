import hmac
import hashlib
from typing import Dict, Optional

# Global dictionary mapping device IDs to their expected HMAC signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries – in practice these would be securely stored.
    "device_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "device_002": "6f1ed002ab5595859014ebf0951522d9",
    # Add more device signatures as needed.
}

def process_iot_packet(
    dev_id: str,
    crypto_sign: str,
    packet_content: Dict
) -> Optional[Dict]:
    """
    Authenticate and process a data packet from an IoT device.

    Parameters
    ----------
    dev_id : str
        Unique identifier for the sending IoT device.
    crypto_sign : str
        Cryptographic signature (hex digest) attached to the packet.
    packet_content : dict
        The actual content of the packet.

    Returns
    -------
    dict or None
        The packet content if authentication succeeds; otherwise None.

    Raises
    ------
    ConnectionError
        If there is a simulated issue receiving data from the device.
    """
    # Simulate a possible connection error (e.g., packet lost or network failure).
    # In a real implementation, this would be triggered by actual I/O exceptions.
    if not isinstance(packet_content, dict):
        raise ConnectionError("Failed to receive valid packet content from device.")

    # Retrieve the expected signature for this device.
    expected_sign = TRUSTED_DEVICE_SIGNATURES.get(dev_id)
    if expected_sign is None:
        # Unknown device – reject the packet.
        return None

    # Perform a constant‑time comparison to mitigate timing attacks.
    if not hmac.compare_digest(expected_sign, crypto_sign):
        # Signature does not match – reject the packet.
        return None

    # At this point, authentication succeeded; safely return the content.
    return packet_content