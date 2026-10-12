import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their expected signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (hex-encoded HMAC values)
    "device_001": "a3f5c2e1d9b4c6e8f7a0b1c3d2e4f5a6",
    "device_002": "b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6",
    # Add real signatures here
}

def validate_device_packet(
    iot_device_id: str,
    iot_signature: str,
    iot_data: Dict
) -> Optional[Dict]:
    """
    Validate an IoT device packet and return processed data.

    Parameters
    ----------
    iot_device_id : str
        Unique identifier of the IoT device.
    iot_signature : str
        Cryptographic signature sent with the packet (hex-encoded).
    iot_data : dict
        The data payload of the packet.

    Returns
    -------
    dict or None
        Processed data dictionary if validation succeeds, otherwise None.

    Raises
    ------
    ConnectionError
        If the packet could not be received (e.g., data is None).
    """
    # Simulate a failure to receive the packet
    if iot_data is None:
        raise ConnectionError(f"Packet from device '{iot_device_id}' could not be received.")

    # Ensure the device is trusted
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(iot_device_id)
    if not expected_sig:
        # Unknown device – reject the packet
        return None

    # Perform a constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(iot_signature, expected_sig):
        # Signature mismatch – reject the packet
        return None

    # At this point, the signature is verified.
    # Perform any necessary processing on the data. For demonstration,
    # we simply add a 'validated' flag.
    processed = dict(iot_data)          # shallow copy to avoid side effects
    processed["validated"] = True
    return processed