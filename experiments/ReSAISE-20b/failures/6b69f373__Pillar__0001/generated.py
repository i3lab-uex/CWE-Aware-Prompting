import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their expected cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with actual device IDs and signatures.
    "device-001": "a3f5c8e9b1d2e4f6",
    "device-002": "7c8d9e0a1b2c3d4f",
    # Add more trusted devices here.
}

def validate_device_packet(
    iot_device_id: str,
    iot_signature: str,
    iot_data: Optional[Dict],
) -> Optional[Dict]:
    """
    Validate and process a data packet from an IoT device.

    Parameters
    ----------
    iot_device_id : str
        Unique identifier of the IoT device sending the data.
    iot_signature : str
        Cryptographic signature accompanying the packet.
    iot_data : dict or None
        Payload of the data packet.

    Returns
    -------
    dict or None
        The processed data if validation succeeds; otherwise, None.

    Raises
    ------
    ConnectionError
        If the packet cannot be received (e.g., data is None or device ID unknown).
    """
    # Basic sanity checks
    if iot_data is None:
        raise ConnectionError("No data received from device.")

    # Ensure the device ID is known
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(iot_device_id)
    if expected_signature is None:
        raise ConnectionError(f"Unknown device ID: {iot_device_id}")

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(iot_signature, expected_signature):
        # Signature mismatch – do not process the data
        return None

    # At this point, signature is valid; proceed with processing.
    # For demonstration purposes, we simply return the data unchanged.
    # In a real implementation, this is where you'd parse, validate,
    # and transform the payload as required by your application.
    return iot_data