import hmac
from typing import Dict, Optional

# Global mapping of trusted device IDs to their expected cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (replace with real values in production)
    "device-001": "a1b2c3d4e5f6g7h8i9j0",
    "device-002": "0123456789abcdef1234",
}


def verify_iot_signature(
    iot_id: str, crypto_signature: str, packet_info: Optional[Dict]
) -> Optional[Dict]:
    """
    Authenticate an IoT data packet by verifying its cryptographic signature.

    Args:
        iot_id (str): Unique identifier of the IoT device.
        crypto_signature (str): Signature attached to the packet.
        packet_info (dict): Payload of the packet.

    Returns:
        dict: The original packet data if signature is valid.
        None: If the signature does not match or the device is unknown.

    Raises:
        ConnectionError: If packet_info is None, simulating a data retrieval failure.
    """
    # Simulate an issue receiving data from the device
    if packet_info is None:
        raise ConnectionError("Failed to receive data from IoT device")

    # Retrieve the expected signature for this device
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(iot_id)

    # If the device is not recognized, reject the packet
    if expected_signature is None:
        return None

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(crypto_signature, expected_signature):
        return None

    # Signature verified – return the packet data
    return packet_info