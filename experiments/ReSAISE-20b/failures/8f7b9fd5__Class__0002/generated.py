import hmac
from typing import Dict, Optional

# Global dictionary mapping device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; in production these would be securely stored.
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef1234",
}

def _receive_packet(device_id: str, packet_signature: str) -> None:
    """
    Simulate receiving a packet. In a real system this would involve I/O.
    Raises ConnectionError if the device is unreachable or the packet cannot be received.
    """
    # For demonstration, we assume all devices are reachable. Replace with real checks.
    if device_id not in TRUSTED_DEVICE_SIGNATURES:
        raise ConnectionError(f"Device {device_id} is unreachable or not registered.")


def process_packet(
    device_id: str,
    packet_signature: str,
    data_packet: Optional[Dict],
) -> Optional[Dict]:
    """
    Validate the cryptographic signature of an IoT data packet and process it.

    Parameters
    ----------
    device_id : str
        Unique identifier for the IoT device sending the data.
    packet_signature : str
        Cryptographic signature accompanying the packet.
    data_packet : dict | None
        The content of the data packet to be processed.

    Returns
    -------
    dict | None
        Processed data if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the packet from the device cannot be received successfully.
    """
    # 1. Ensure we can receive the packet (simulated).
    _receive_packet(device_id, packet_signature)

    # 2. Basic validation of inputs.
    if data_packet is None or not isinstance(data_packet, dict):
        return None

    # 3. Retrieve the trusted signature for this device.
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not expected_signature:
        # Device is unknown; reject the packet.
        return None

    # 4. Use constant‑time comparison to prevent timing attacks.
    if not hmac.compare_digest(packet_signature, expected_signature):
        # Signature mismatch; reject the packet.
        return None

    # 5. Process the data (example: add a processed flag and timestamp).
    processed_data = dict(data_packet)  # shallow copy to avoid mutating input
    processed_data["processed"] = True
    processed_data["device_id"] = device_id

    return processed_data