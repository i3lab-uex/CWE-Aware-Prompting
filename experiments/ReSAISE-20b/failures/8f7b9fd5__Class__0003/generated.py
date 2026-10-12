import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their expected cryptographic signatures.
# In a real system this would be stored securely and likely retrieved
# from a database or key management service.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "z9y8x7w6v5u4t3s2r1q0",
    # ... more device signatures ...
}


def process_packet(
    device_id: str,
    packet_signature: str,
    data_packet: Optional[Dict],
) -> Optional[Dict]:
    """
    Validate the packet signature and process the data.

    Parameters
    ----------
    device_id : str
        Unique identifier for the IoT device sending the data.
    packet_signature : str
        Cryptographic signature sent along with the packet.
    data_packet : dict | None
        The content of the data packet to be processed.

    Returns
    -------
    dict | None
        The processed data if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the packet could not be received successfully (e.g., missing data).
    """
    # Ensure we have a packet to process.
    if data_packet is None:
        raise ConnectionError(f"Failed to receive data packet from device {device_id}")

    # Retrieve the expected signature for this device.
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not expected_signature:
        # Unknown device – treat as unauthenticated.
        return None

    # Perform a constant‑time comparison to mitigate timing attacks.
    if not hmac.compare_digest(packet_signature, expected_signature):
        # Signature mismatch – reject the packet.
        return None

    # At this point, the packet is authenticated. Perform any desired
    # processing. For illustration, we simply return a copy of the data.
    processed_data = dict(data_packet)  # shallow copy to avoid mutation
    return processed_data