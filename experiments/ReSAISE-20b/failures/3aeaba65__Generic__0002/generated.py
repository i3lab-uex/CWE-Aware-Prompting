import hmac
from typing import Dict, Optional

# Global dictionary mapping device IDs to their expected cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; in a real system these would be securely stored.
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "0z9y8x7w6v5u4t3s2r1q",
    # Add more trusted device signatures as needed.
}

def verify_iot_signature(
    iot_id: str,
    crypto_signature: str,
    packet_info: Dict
) -> Optional[Dict]:
    """
    Authenticate and process a data packet from an IoT device.

    Parameters
    ----------
    iot_id : str
        Unique identifier of the IoT device sending the data.
    crypto_signature : str
        Cryptographic signature attached to the packet.
    packet_info : dict
        The actual content of the data packet.

    Returns
    -------
    dict | None
        Returns `packet_info` if the signature is valid, otherwise `None`.

    Raises
    ------
    ConnectionError
        If an issue occurs while receiving data from the device.
    """
    # Simulate a potential communication error. In a real implementation,
    # this would be replaced by actual network exception handling.
    if packet_info is None:
        raise ConnectionError("Failed to receive data from IoT device")

    # Retrieve the expected signature for this device.
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(iot_id)

    # If the device is not registered or the signature does not match,
    # authentication fails.
    if expected_signature is None:
        return None

    # Use a constant-time comparison to mitigate timing attacks.
    if hmac.compare_digest(expected_signature, crypto_signature):
        return packet_info

    # Signature mismatch: do not trust the data.
    return None