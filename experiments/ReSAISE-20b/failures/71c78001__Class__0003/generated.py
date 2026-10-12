import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    "device_001": "a1b2c3d4e5f6",
    "device_002": "deadbeef1234",
    # Add more device signatures as needed.
}

def process_iot_packet(
    dev_id: str,
    crypto_sign: str,
    packet_content: Dict
) -> Optional[Dict]:
    """
    Validate the cryptographic signature of an IoT packet and return its content.

    Parameters
    ----------
    dev_id : str
        Unique identifier of the sending IoT device.
    crypto_sign : str
        Cryptographic signature attached to the packet.
    packet_content : dict
        The actual data payload of the packet.

    Returns
    -------
    dict or None
        The packet content if signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If there was an issue receiving data from the IoT device.
    """
    # Simulate a potential connectivity issue (placeholder for real I/O logic).
    if not isinstance(dev_id, str) or not dev_id:
        raise ConnectionError("Failed to receive data: invalid device identifier")

    # Retrieve the trusted signature for this device.
    expected_sign = TRUSTED_DEVICE_SIGNATURES.get(dev_id)

    if expected_sign is None:
        # Unknown device; cannot trust the packet.
        return None

    # Use a constant-time comparison to mitigate timing attacks (CWE-345).
    if hmac.compare_digest(expected_sign, crypto_sign):
        # Signature matches; return the packet content.
        return packet_content
    else:
        # Signature mismatch; discard data.
        return None