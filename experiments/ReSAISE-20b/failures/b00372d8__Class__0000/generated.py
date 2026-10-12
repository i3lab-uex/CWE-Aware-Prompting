import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their expected cryptographic signatures.
# In a real system these would be securely stored and managed.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    "device-001": "a1b2c3d4e5f6g7h8i9j0",
    "device-002": "b1c2d3e4f5g6h7i8j9k0",
    # ... additional device signatures
}

def process_iot_packet(
    device_id: str,
    crypt_sig: str,
    pkt_data: Dict
) -> Optional[Dict]:
    """
    Validate the cryptographic signature of an IoT packet and process its data.

    Parameters
    ----------
    device_id : str
        Unique identifier of the IoT device sending the packet.
    crypt_sig : str
        Cryptographic signature accompanying the packet.
    pkt_data : dict
        Payload of the IoT data packet.

    Returns
    -------
    Optional[dict]
        The processed data if the signature is valid; otherwise None.

    Raises
    ------
    ConnectionError
        If the packet cannot be received (simulated here as a generic error).
    """
    # Simulate a possible network failure
    try:
        # In real code this would involve I/O operations that could raise errors.
        pass
    except Exception as exc:
        # Wrap any low‑level exception in a ConnectionError for clarity.
        raise ConnectionError("Failed to receive packet.") from exc

    # Retrieve the expected signature for this device.
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)

    # If the device is unknown, reject the packet.
    if expected_sig is None:
        return None

    # Use constant‑time comparison to prevent timing attacks.
    if not hmac.compare_digest(crypt_sig, expected_sig):
        # Signature does not match; reject the packet.
        return None

    # At this point, authenticity is verified. Perform any additional
    # processing required by the application. For demonstration purposes,
    # we simply return the packet data unchanged.
    return pkt_data