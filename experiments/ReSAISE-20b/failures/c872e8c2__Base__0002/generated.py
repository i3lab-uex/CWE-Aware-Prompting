import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their trusted signatures.
# In a real system these would be securely stored and rotated regularly.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    "device-001": "a1b2c3d4e5f6g7h8i9j0",
    "device-002": "1234567890abcdef1234",
    # Add more device signatures as needed.
}

def manage_data_packet(
    io_device_id: str,
    crypto_signature: str,
    packet_data: Dict
) -> Optional[Dict]:
    """
    Validate and process an incoming data packet from an IoT device.

    Parameters
    ----------
    io_device_id : str
        The unique identifier of the IoT device that sent the packet.
    crypto_signature : str
        The cryptographic signature attached to the packet.
    packet_data : dict
        The actual data or payload to be processed.

    Returns
    -------
    dict | None
        The packet data if the signature is verified successfully,
        otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the packet could not be received (e.g., missing device ID or signature).
    """
    # Simulate a scenario where packet reception fails
    if io_device_id is None or crypto_signature is None:
        raise ConnectionError("Failed to receive packet from device.")

    # Retrieve the trusted signature for this device
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(io_device_id)
    if expected_sig is None:
        # Unknown device: treat as untrusted
        return None

    # Use constant‑time comparison to mitigate timing attacks (CWE-347)
    if not hmac.compare_digest(expected_sig, crypto_signature):
        # Signature does not match
        return None

    # Signature verified – process and return the data.
    # In a real application, further validation of packet_data would be performed here.
    return packet_data