import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their trusted cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries – in a real system these would be securely stored.
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef",
}

def process_iot_packet(
    dev_id: str,
    crypto_sign: str,
    packet_content: Dict
) -> Optional[Dict]:
    """
    Validate the cryptographic signature of an IoT data packet and return
    its content if authenticated.

    Parameters
    ----------
    dev_id : str
        Unique identifier of the IoT device.
    crypto_sign : str
        Cryptographic signature attached to the packet.
    packet_content : dict
        The actual data payload of the packet.

    Returns
    -------
    dict | None
        Returns `packet_content` if signature is valid, otherwise `None`.

    Raises
    ------
    ConnectionError
        If the packet content cannot be retrieved (e.g., missing or corrupted).
    """
    # Simulate a potential data retrieval failure
    if packet_content is None:
        raise ConnectionError(f"Failed to receive data from device {dev_id}")

    # Retrieve the trusted signature for this device
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(dev_id)
    if not expected_sig:
        # Unknown device – treat as unauthenticated
        return None

    # Use constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(expected_sig, crypto_sign):
        # Signature mismatch – do not trust the data
        return None

    # All checks passed; return the packet content
    return packet_content