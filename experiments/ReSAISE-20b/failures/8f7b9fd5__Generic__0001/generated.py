import hmac
import random
from typing import Dict, Optional

# Global mapping of device IDs to their expected cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (in a real system these would be securely stored)
    "device_001": "5f2c9d1a3b4e6f8a7c0d9e1f2a3b4c5d",
    "device_002": "7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d",
    # Add more trusted device signatures here
}

def process_packet(device_id: str, packet_signature: str, data_packet: Dict) -> Optional[Dict]:
    """
    Validate and process an IoT device packet.

    Parameters
    ----------
    device_id : str
        Unique identifier for the sending IoT device.
    packet_signature : str
        Cryptographic signature accompanying the packet.
    data_packet : dict
        Payload of the packet to be processed.

    Returns
    -------
    dict | None
        Processed data if validation succeeds; otherwise, None.

    Raises
    ------
    ConnectionError
        If the packet cannot be received due to a simulated network failure.
    """
    # Simulate potential network unreliability
    if random.random() < 0.05:   # 5% chance of failure
        raise ConnectionError(f"Failed to receive packet from device {device_id}")

    # Retrieve the expected signature for this device
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(device_id)

    # If the device is unknown or has no registered signature, reject
    if expected_signature is None:
        return None

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(packet_signature, expected_signature):
        return None

    # At this point the signature is verified; process the data.
    # For demonstration, we simply return a copy of the packet enriched with metadata.
    processed = dict(data_packet)  # shallow copy to avoid mutating the input
    processed.update({
        "device_id": device_id,
        "verified_at": "2026-07-23T12:00:00Z",  # placeholder timestamp
    })

    return processed

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     packet = {"temperature": 22.5, "humidity": 45}
#     signature = TRUSTED_DEVICE_SIGNATURES["device_001"]
#     try:
#         result = process_packet("device_001", signature, packet)
#         print(result)
#     except ConnectionError as e:
#         print(e)