import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their trusted cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (replace with real signatures in production)
    "device-001": "a1b2c3d4e5f6g7h8i9j0",
    "device-002": "1234567890abcdef",
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
        Cryptographic signature attached to the packet.
    packet_content : dict
        The actual data payload of the packet.

    Returns
    -------
    dict or None
        Returns `packet_content` if the signature is valid.
        Otherwise returns ``None``.

    Raises
    ------
    ConnectionError
        If there is an issue receiving data from the IoT device.
    """
    # Simulate a potential failure in receiving data
    if packet_content is None:
        raise ConnectionError("Failed to receive data from device")

    # Retrieve the trusted signature for this device
    trusted_sig = TRUSTED_DEVICE_SIGNATURES.get(dev_id)
    if trusted_sig is None:
        # Device not recognized
        return None

    # Constant‑time comparison to prevent timing attacks
    if hmac.compare_digest(crypto_sign, trusted_sig):
        # Signature is valid – return the packet content
        return packet_content

    # Invalid signature
    return None