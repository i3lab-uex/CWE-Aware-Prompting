import hmac
import hashlib
from typing import Dict, Optional

# Global mapping of device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, bytes] = {
    # Example entries – replace with actual device ID → signature mappings.
    "device_001": b"5f2d7a9c8e1b4f6a3d9c0f2b5a7e8c1d",
    "device_002": b"9c3b2a1f4e5d6c7b8a0f9e8d7c6b5a4",
}

def _verify_signature(
    device_id: str, expected_sig_hex: bytes, actual_sig_hex: str
) -> bool:
    """
    Verify that the provided signature matches the expected one for the device.
    Uses constant‑time comparison to mitigate timing attacks.
    """
    try:
        # Convert the provided signature from hex string to bytes
        actual_sig = bytes.fromhex(actual_sig_hex)
    except ValueError:
        # Malformed signature
        return False

    # Constant‑time comparison
    return hmac.compare_digest(expected_sig_hex, actual_sig)

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
        Cryptographic signature attached to the packet (hex string).
    packet_data : dict
        The actual data or payload to be processed.

    Returns
    -------
    dict | None
        The packet data if the signature is verified; otherwise, None.

    Raises
    ------
    ConnectionError
        If the packet data is missing or cannot be processed.
    """
    if not isinstance(packet_data, dict):
        raise ConnectionError("Invalid packet data: expected a dictionary.")

    # Retrieve the trusted signature for this device
    expected_sig_hex = TRUSTED_DEVICE_SIGNATURES.get(io_device_id)
    if expected_sig_hex is None:
        # Unknown device – treat as a connection issue
        raise ConnectionError(f"Unknown IoT device: {io_device_id}")

    # Verify the signature
    if not _verify_signature(io_device_id, expected_sig_hex, crypto_signature):
        # Signature mismatch – do not trust the data
        return None

    # At this point, the packet is considered authentic.
    # Further processing logic would go here (e.g., storing data, triggering actions).
    return packet_data