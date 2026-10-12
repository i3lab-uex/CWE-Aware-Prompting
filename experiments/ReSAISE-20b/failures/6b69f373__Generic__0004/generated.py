import hmac
from typing import Dict, Optional

# Global dictionary mapping device IDs to their expected cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (in practice these would be securely stored and managed)
    "device_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "device_002": "e99a18c428cb38d5f260853678922e03",
    # Add more trusted devices as needed
}

def validate_device_packet(
    iot_device_id: str,
    iot_signature: str,
    iot_data: Dict
) -> Optional[Dict]:
    """
    Validate and process a data packet from an IoT device.

    Parameters
    ----------
    iot_device_id : str
        Unique identifier of the sending IoT device.
    iot_signature : str
        Cryptographic signature included with the packet.
    iot_data : dict
        Payload of the data packet.

    Returns
    -------
    dict | None
        The original data dictionary if validation succeeds, otherwise None.

    Raises
    ------
    ConnectionError
        If the packet cannot be received (e.g., data is missing or empty).
    """
    # Ensure that the packet was actually received.
    if iot_data is None or not isinstance(iot_data, dict):
        raise ConnectionError("Failed to receive a valid data packet from the device.")

    # Retrieve the expected signature for this device.
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(iot_device_id)
    if not expected_signature:
        # Device is unknown or not trusted.
        return None

    # Use constant‑time comparison to mitigate timing attacks.
    if not hmac.compare_digest(iot_signature, expected_signature):
        # Signature mismatch – treat as a potential spoofing attempt.
        return None

    # At this point, the packet is authenticated.  Return the data unchanged.
    return iot_data