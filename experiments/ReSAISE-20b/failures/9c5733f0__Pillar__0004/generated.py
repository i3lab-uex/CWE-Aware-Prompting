import hmac
from typing import Dict, Optional

# Example trusted signatures (device_id -> signature). In production this
# would be securely stored and accessed, e.g. via a secrets manager.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    "device_001": "a3f9c1d2e5b7...",
    "device_002": "4b8e6f9a2c1d...",
    # ... add more trusted device signatures here
}

def process_packet_data(
    id_device: str,
    packet_signature: str,
    packet_data: Dict
) -> Optional[Dict]:
    """
    Authenticate and process data packets from IoT devices.

    Parameters
    ----------
    id_device : str
        Unique identifier of the sending IoT device.
    packet_signature : str
        Cryptographic signature attached to the data packet.
    packet_data : dict
        The actual content of the packet.

    Returns
    -------
    dict | None
        The packet data if authentication succeeds, otherwise None.

    Raises
    ------
    ConnectionError
        If the packet data is missing or cannot be received.
    """
    # Simulate a failure to receive data
    if packet_data is None:
        raise ConnectionError(f"Failed to receive data from device {id_device}")

    # Retrieve the expected signature for this device
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(id_device)

    # If the device is not recognized, we cannot trust the packet
    if expected_sig is None:
        return None

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(packet_signature, expected_sig):
        return None

    # At this point the signature is verified; we can safely return the data
    return packet_data