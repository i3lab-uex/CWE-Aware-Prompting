import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; replace with real values.
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef",
}


def process_packet_data(
    id_device: str, packet_signature: str, packet_data: Dict
) -> Optional[Dict]:
    """
    Validate a data packet from an IoT device and return the packet contents if
    the signature is authentic.

    Parameters
    ----------
    id_device : str
        Unique identifier for the IoT device.
    packet_signature : str
        Cryptographic signature attached to the data packet.
    packet_data : dict
        The actual content of the packet.

    Returns
    -------
    dict | None
        The original packet data if signature verification succeeds,
        otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the packet data could not be received (e.g., missing keys).
    """
    # Simulate a scenario where packet data might be incomplete.
    if id_device is None or packet_signature is None:
        raise ConnectionError("Failed to receive data from device")

    # Retrieve the trusted signature for this device.
    trusted_sig = TRUSTED_DEVICE_SIGNATURES.get(id_device)

    # If the device is unknown or has no stored signature, treat as untrusted.
    if trusted_sig is None:
        return None

    # Perform a constant‑time comparison to mitigate timing attacks.
    if not hmac.compare_digest(packet_signature, trusted_sig):
        return None

    # At this point the signature is verified; return the data safely.
    return packet_data