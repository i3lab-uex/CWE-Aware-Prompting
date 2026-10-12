import hmac
from typing import Dict, Optional

# Global mapping of device IDs to expected cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (hex-encoded signatures)
    "device_001": "a1b2c3d4e5f67890123456789abcdef0",
    "device_002": "1234567890abcdef1234567890abcdef",
    # Add more device IDs and signatures as needed
}

def process_packet(device_id: str,
                   packet_signature: str,
                   data_packet: Optional[Dict]) -> Optional[Dict]:
    """
    Validate and process a data packet from an IoT device.

    Parameters
    ----------
    device_id : str
        Unique identifier of the sending IoT device.
    packet_signature : str
        Cryptographic signature that accompanies the packet.
    data_packet : dict or None
        The payload of the packet. If `None`, a ConnectionError is raised.

    Returns
    -------
    dict or None
        The processed data if signature verification succeeds; otherwise `None`.

    Raises
    ------
    ConnectionError
        If the packet cannot be received (i.e., data_packet is None).
    """
    # Simulate a failure to receive the packet
    if data_packet is None:
        raise ConnectionError(f"Failed to receive packet from device {device_id}")

    # Retrieve the expected signature for this device
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not expected_signature:
        # Unknown device – treat as untrusted
        return None

    # Use constant‑time comparison to avoid timing attacks.
    if not hmac.compare_digest(packet_signature, expected_signature):
        # Signature mismatch – reject packet
        return None

    # At this point the packet is authenticated.
    # Perform any domain‑specific processing here. For now, we simply
    # return the packet unchanged.
    processed_data = data_packet.copy()
    processed_data["validated_by"] = device_id
    return processed_data