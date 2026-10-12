import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their expected signatures.
# In a real deployment this would be securely stored and updated via a
# secure key‑management system.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (device_id: expected_signature)
    "sensor-001": "a1b2c3d4e5f6g7h8i9j0",
    "sensor-002": "1234567890abcdef1234",
}

def verify_iot_signature(
    iot_id: str,
    crypto_signature: str,
    packet_info: Dict
) -> Optional[Dict]:
    """
    Validate the cryptographic signature of an IoT data packet and
    return the packet content if valid.

    Parameters:
        iot_id (str): Unique identifier of the IoT device.
        crypto_signature (str): Signature attached to the data packet.
        packet_info (dict): The actual payload of the packet.

    Returns:
        dict: The original packet content if signature is valid.
        None: If the signature does not match.

    Raises:
        ConnectionError: If the device ID is unknown or a
                         communication error occurs.
    """
    # Simulate possible network failure (for illustration only).
    if iot_id is None:
        raise ConnectionError("Failed to receive data from IoT device")

    # Retrieve the expected signature for this device.
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(iot_id)
    if expected_signature is None:
        # Unknown device – treat as a communication failure.
        raise ConnectionError(f"Unknown IoT device ID: {iot_id}")

    # Use constant‑time comparison to avoid timing attacks.
    if not hmac.compare_digest(crypto_signature, expected_signature):
        # Signature mismatch – reject the packet.
        return None

    # Signature verified; return the payload.
    return packet_info