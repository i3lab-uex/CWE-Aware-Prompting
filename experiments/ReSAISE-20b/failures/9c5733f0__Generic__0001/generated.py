import hmac
from typing import Dict, Optional

# Global dictionary mapping device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with real device IDs and signatures.
    "device_001": "a3f1c8e5d4b2",
    "device_002": "9b7e6a1c3d4f",
}

def process_packet_data(
    id_device: str,
    packet_signature: str,
    packet_data: Optional[Dict],
) -> Optional[Dict]:
    """
    Authenticate and process a data packet from an IoT device.

    Parameters
    ----------
    id_device : str
        Unique identifier for the sending IoT device.
    packet_signature : str
        Cryptographic signature attached to the data packet.
    packet_data : dict or None
        The actual content of the packet. If `None`, it indicates a failure to
        receive data from the device.

    Returns
    -------
    dict or None
        The packet data if the signature is valid; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the packet data could not be received from the device.
    """
    # Simulate a failure to receive data
    if packet_data is None:
        raise ConnectionError(f"Failed to receive data from device {id_device}")

    # Retrieve the trusted signature for this device
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(id_device)
    if not expected_signature:
        # Unknown device – treat as untrusted
        return None

    # Perform a constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(packet_signature, expected_signature):
        # Signature does not match – data is untrusted
        return None

    # All checks passed; return the packet data
    return packet_data