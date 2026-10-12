import hmac
from typing import Dict, Optional

# Global dictionary mapping device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (replace with real signatures)
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef1234",
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
        Unique identifier of the IoT device that sent the packet.
    crypto_signature : str
        Cryptographic signature attached to the packet.
    packet_data : dict
        The actual data or payload to be processed.

    Returns
    -------
    dict | None
        The packet data if the signature is verified; otherwise, None.

    Raises
    ------
    ConnectionError
        If any of the required arguments are missing or invalid, simulating a failure to receive data.
    """
    # Basic sanity checks – in real code this would be more elaborate
    if not all([io_device_id, crypto_signature, packet_data]):
        raise ConnectionError("Failed to receive a complete data packet.")

    # Retrieve the trusted signature for this device
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(io_device_id)
    if not expected_signature:
        # Unknown device – treat as a failed connection
        raise ConnectionError(f"Unknown device ID: {io_device_id}")

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(crypto_signature, expected_signature):
        # Signature mismatch – packet cannot be trusted
        return None

    # At this point the signature is verified; return the payload
    return packet_data