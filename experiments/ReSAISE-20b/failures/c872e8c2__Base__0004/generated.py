import hashlib
import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their trusted signatures (hex-encoded)
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; in a real system these would be securely stored
    "device_001": "a3f1c2d4e5b6f7a8b9c0d1e2f3a4b5c6",
    "device_002": "deadbeef1234567890abcdef12345678",
}


def _verify_signature(
    expected_sig_hex: str, actual_sig_hex: str
) -> bool:
    """
    Compare two hex-encoded signatures in constant time to avoid timing attacks.
    """
    try:
        expected = bytes.fromhex(expected_sig_hex)
        actual = bytes.fromhex(actual_sig_hex)
    except ValueError:
        # Invalid hex encoding
        return False

    return hmac.compare_digest(expected, actual)


def manage_data_packet(
    io_device_id: str,
    crypto_signature: str,
    packet_data: Dict,
) -> Optional[Dict]:
    """
    Validate and process an incoming data packet from an IoT device.

    Parameters
    ----------
    io_device_id : str
        Unique identifier of the IoT device that sent the packet.
    crypto_signature : str
        Cryptographic signature (hex-encoded) attached to the packet.
    packet_data : dict
        The actual data or payload to be processed.

    Returns
    -------
    dict | None
        The packet_data dictionary if the signature is verified; otherwise, None.

    Raises
    ------
    ConnectionError
        If packet_data is missing or any other issue occurs while receiving the packet.
    """
    # Basic validation of input
    if not isinstance(io_device_id, str) or not io_device_id:
        raise ValueError("Invalid device ID")

    if not isinstance(crypto_signature, str) or not crypto_signature:
        raise ValueError("Invalid cryptographic signature")

    if packet_data is None or not isinstance(packet_data, dict):
        # Simulate an issue in receiving the packet
        raise ConnectionError("Failed to receive a valid data packet")

    # Retrieve the trusted signature for this device
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(io_device_id)

    if not expected_sig:
        # Device is unknown; treat as untrusted
        return None

    # Verify the signature using constant-time comparison
    if not _verify_signature(expected_sig, crypto_signature):
        # Signature mismatch – do not trust the data
        return None

    # At this point, the signature is verified; return the packet data
    return packet_data