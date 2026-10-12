import hmac
from typing import Dict, Optional

# Global dictionary containing the expected signature for each trusted device.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (in practice these would be securely stored)
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "z9y8x7w6v5u4t3s2r1q0",
    # ... add more device IDs and their expected signatures
}


def validate_device_packet(
    iot_device_id: str,
    iot_signature: str,
    iot_data: Optional[Dict],
) -> Optional[Dict]:
    """
    Validate an IoT device packet and return the processed data.

    Parameters
    ----------
    iot_device_id : str
        Unique identifier of the device sending the packet.
    iot_signature : str
        Cryptographic signature included with the packet.
    iot_data : dict | None
        The payload of the packet.

    Returns
    -------
    dict | None
        The processed data if signature validation succeeds, otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the packet cannot be received successfully (i.e., ``iot_data`` is ``None``).
    """
    # Simulate the possibility of a packet not being received.
    if iot_data is None:
        raise ConnectionError("Failed to receive packet from device.")

    # Retrieve the expected signature for this device.
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(iot_device_id)
    if expected_sig is None:
        # Unknown device – treat as a failure.
        return None

    # Constant‑time comparison to avoid timing attacks (CWE-693).
    if not hmac.compare_digest(iot_signature, expected_sig):
        return None

    # At this point the packet is authenticated.
    # In a real implementation you might perform additional processing here.
    return iot_data