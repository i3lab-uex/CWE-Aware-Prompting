import hmac
from typing import Dict, Optional

# Global dictionary containing trusted signatures for each device.
# In a real system this would be securely stored and rotated regularly.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1a2b3c4d5e6f7g8h9i0j",
    # Add more device_id:signature pairs as needed
}

def process_packet(device_id: str, packet_signature: str, data_packet: Dict) -> Optional[Dict]:
    """
    Validate a packet from an IoT device and return the processed data.

    Parameters
    ----------
    device_id : str
        Unique identifier of the IoT device.
    packet_signature : str
        Cryptographic signature attached to the data packet.
    data_packet : dict
        Payload of the IoT device.

    Returns
    -------
    Optional[dict]
        The processed data if the signature is valid, otherwise None.

    Raises
    ------
    ConnectionError
        If the device_id is not known or if no data_packet was received.
    """
    # Simulate a failure to receive the packet
    if data_packet is None:
        raise ConnectionError(f"Failed to receive packet from device {device_id}")

    # Retrieve the expected signature for this device
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if expected_signature is None:
        # Unknown device; treat as a connection issue
        raise ConnectionError(f"Unknown device ID: {device_id}")

    # Perform a timing‑safe comparison to avoid leaking information
    if not hmac.compare_digest(packet_signature, expected_signature):
        # Signature mismatch: treat as invalid data
        return None

    # At this point the packet is authenticated.
    # Additional processing can be performed here; for now we simply return it.
    processed_data = dict(data_packet)  # shallow copy to avoid side‑effects
    return processed_data