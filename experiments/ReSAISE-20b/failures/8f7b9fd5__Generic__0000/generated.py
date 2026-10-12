import hmac
from typing import Dict, Optional

# Global dictionary mapping device IDs to their expected cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (device_id: expected_signature)
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef0123",
    # Add more trusted device signatures here.
}

def process_packet(
    device_id: str,
    packet_signature: str,
    data_packet: Optional[Dict]
) -> Optional[Dict]:
    """
    Validate the cryptographic signature of an incoming data packet from an IoT device
    and process the packet if the signature is authentic.

    Args:
        device_id (str): Unique identifier of the sending IoT device.
        packet_signature (str): Signature accompanying the data packet.
        data_packet (dict | None): The payload to be processed.

    Returns:
        dict | None: Processed data dictionary if validation succeeds, otherwise None.

    Raises:
        ConnectionError: If the packet cannot be received successfully
                         (e.g., data_packet is None or empty).
    """
    # 1. Ensure packet was received
    if data_packet is None:
        raise ConnectionError("Packet could not be received from device '{}'.".format(device_id))

    # 2. Retrieve the expected signature for this device
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if expected_signature is None:
        # Unknown device: treat as invalid
        return None

    # 3. Verify signature using a constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(packet_signature, expected_signature):
        # Signature mismatch – reject packet
        return None

    # 4. Process the data (example: add a processing flag and timestamp)
    processed = dict(data_packet)  # shallow copy to avoid mutating input
    processed["processed"] = True

    return processed