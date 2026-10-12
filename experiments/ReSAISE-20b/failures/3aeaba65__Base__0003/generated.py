import hmac
import hashlib

# Global dictionary containing the expected signature for each trusted device.
# In a real system this would be populated from a secure source (e.g., a database or
# an encrypted configuration file). The values are hex-encoded SHA256 HMACs.
TRUSTED_DEVICE_SIGNATURES = {
    "device_001": "a3f1c9e2d4b7e8f0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f67890abcdef123456",
    "device_002": "b2c3d4e5f67890abcdef123456a3f1c9e2d4b7e8f0c1d2e3f4a5b6c7d8e9f0",
    # Add more devices here
}

def _verify_signature(expected_sig: str, actual_sig: str) -> bool:
    """
    Compare two signatures in constant time to avoid timing attacks.
    The function accepts hex-encoded strings and compares them as bytes.
    """
    try:
        expected_bytes = bytes.fromhex(expected_sig)
        actual_bytes = bytes.fromhex(actual_sig)
    except ValueError:
        # Invalid hex string – treat as verification failure
        return False

    return hmac.compare_digest(expected_bytes, actual_bytes)

def verify_iot_signature(iot_id: str, crypto_signature: str, packet_info: dict) -> dict | None:
    """
    Authenticate an IoT data packet by verifying its cryptographic signature.

    Parameters
    ----------
    iot_id : str
        Unique identifier of the IoT device.
    crypto_signature : str
        Hex-encoded cryptographic signature attached to the packet.
    packet_info : dict
        The actual content of the packet to be processed.

    Returns
    -------
    dict | None
        The packet data if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If packet_info is missing or cannot be processed (simulating a network issue).
    """
    # Simulate a failure to receive data from the device
    if packet_info is None:
        raise ConnectionError(f"Failed to receive data from device {iot_id}")

    # Retrieve the expected signature for this device
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(iot_id)
    if not expected_sig:
        # Unknown device – treat as a failed verification
        return None

    # Verify the signature in constant time
    if not _verify_signature(expected_sig, crypto_signature):
        return None

    # At this point the packet is trusted; return it
    return packet_info