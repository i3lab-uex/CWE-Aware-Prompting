import hmac
from typing import Dict, Optional

# Global dictionary mapping device IDs to their expected signatures.
# In a real deployment this would be populated from secure storage.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "0123456789abcdef1234",
}

def validate_device_packet(
    iot_device_id: str,
    iot_signature: str,
    iot_data: Dict
) -> Optional[Dict]:
    """
    Validate and process an IoT device packet.

    Parameters
    ----------
    iot_device_id : str
        Unique identifier of the device that sent the packet.
    iot_signature : str
        Cryptographic signature attached to the packet.
    iot_data : dict
        The payload of the packet.

    Returns
    -------
    dict or None
        The original data dictionary if signature validation succeeds,
        otherwise `None`.

    Raises
    ------
    ConnectionError
        If the packet cannot be received (e.g., `iot_data` is None).
    """
    # Basic sanity checks
    if iot_data is None:
        raise ConnectionError("Packet could not be received from device.")

    # Ensure the device ID is known
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(iot_device_id)
    if expected_sig is None:
        # Unknown device – treat as invalid
        return None

    # Perform a constant‑time comparison to mitigate timing attacks.
    if not hmac.compare_digest(iot_signature, expected_sig):
        # Signature mismatch – packet is untrusted
        return None

    # At this point the packet is authenticated.
    # Here we simply return the data unchanged, but you could
    # perform additional processing or transformation as needed.
    return iot_data