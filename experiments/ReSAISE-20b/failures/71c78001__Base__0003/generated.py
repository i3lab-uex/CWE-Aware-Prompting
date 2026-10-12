import hmac
from typing import Dict, Any

# Global dictionary mapping device IDs to their expected cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (replace with real values)
    "device-001": "a1b2c3d4e5f6g7h8i9j0",
    "device-002": "0z9y8x7w6v5u4t3s2r1q",
}

def process_iot_packet(dev_id: str, crypto_sign: str, packet_content: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Validate the cryptographic signature of an IoT data packet and return its content.

    Parameters
    ----------
    dev_id : str
        Unique identifier of the sending IoT device.
    crypto_sign : str
        Cryptographic signature attached to the packet.
    packet_content : dict
        The actual content of the data packet.

    Returns
    -------
    dict | None
        The packet content if signature verification succeeds, otherwise None.

    Raises
    ------
    ConnectionError
        If the device ID is unknown or packet content could not be retrieved.
    """
    # Basic sanity checks
    if dev_id is None or crypto_sign is None:
        raise ConnectionError("Missing device ID or signature.")
    if packet_content is None:
        # Simulate a failure in receiving data
        raise ConnectionError(f"Failed to receive packet from device '{dev_id}'.")

    # Retrieve the expected signature for this device
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(dev_id)
    if expected_sig is None:
        raise ConnectionError(f"Unknown device ID: {dev_id}")

    # Constant‑time comparison to prevent timing attacks (CWE-347 mitigation)
    if not hmac.compare_digest(expected_sig, crypto_sign):
        # Signature mismatch – treat as unauthenticated data
        return None

    # At this point the signature is verified; trust the packet content
    return packet_content