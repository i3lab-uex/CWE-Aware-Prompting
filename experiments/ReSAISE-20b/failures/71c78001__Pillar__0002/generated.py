import hmac
from typing import Dict, Optional

# Global dictionary mapping device IDs to their expected cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; replace with real values in production.
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "0123456789abcdef1234",
}

def process_iot_packet(
    dev_id: str,
    crypto_sign: str,
    packet_content: Dict
) -> Optional[Dict]:
    """
    Validate a cryptographic signature from an IoT device and return the packet
    content if the signature is trusted.

    Parameters
    ----------
    dev_id : str
        Unique identifier of the IoT device.
    crypto_sign : str
        Cryptographic signature received with the packet.
    packet_content : dict
        The actual data payload of the packet.

    Returns
    -------
    dict | None
        The packet content if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the device ID is unknown or there was an error receiving data.
    """
    # Ensure we have a known device
    if dev_id not in TRUSTED_DEVICE_SIGNATURES:
        raise ConnectionError(f"Unknown device ID: {dev_id}")

    # Retrieve the expected signature for this device
    expected_sign = TRUSTED_DEVICE_SIGNATURES[dev_id]

    # Use constant‑time comparison to mitigate timing attacks (CWE‑693)
    if not hmac.compare_digest(expected_sign, crypto_sign):
        return None

    # Signature is valid; return the payload
    return packet_content