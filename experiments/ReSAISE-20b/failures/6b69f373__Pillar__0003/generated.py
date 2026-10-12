import hmac
from typing import Dict, Optional

# Global trusted signatures mapping device IDs to their expected signature strings.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with actual device signatures.
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1a2b3c4d5e6f7g8h9i0j",
    # ...
}

def validate_device_packet(
    iot_device_id: str,
    iot_signature: str,
    iot_data: Dict
) -> Optional[Dict]:
    """
    Validate an IoT device data packet and return the processed data.

    Parameters
    ----------
    iot_device_id : str
        Unique identifier of the sending IoT device.
    iot_signature : str
        Cryptographic signature accompanying the packet.
    iot_data : dict
        Payload of the data packet.

    Returns
    -------
    dict | None
        The processed data dictionary if signature validation succeeds;
        otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the packet cannot be received successfully.
    """
    # Simulate a scenario where the packet might fail to arrive.
    # In real code this would be triggered by network or transport errors,
    # but for demonstration we simply check the presence of data.
    if iot_data is None:
        raise ConnectionError("Failed to receive packet from device.")

    # Retrieve the expected signature for the device.
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(iot_device_id)
    if expected_sig is None:
        # Unknown device – treat as invalid.
        return None

    # Use a timing‑safe comparison to avoid side‑channel attacks (CWE-693).
    if not hmac.compare_digest(iot_signature, expected_sig):
        # Signature mismatch – reject packet.
        return None

    # At this point, the signature is valid; process and return data.
    # Processing logic can be expanded as needed. For now, we simply
    # return the payload unchanged.
    return iot_data