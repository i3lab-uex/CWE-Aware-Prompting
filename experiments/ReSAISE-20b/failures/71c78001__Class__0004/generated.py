import hmac
import hashlib
import random

# Global dictionary mapping device IDs to their known valid signatures (hex strings)
TRUSTED_DEVICE_SIGNATURES = {
    "device_001": "5e884898da28047151d0e56f8dc6292773603d0d6aabbddc4b5b3e2f6e6a8e3d",
    "device_002": "7c222fb2927d2b9f8aa3e5f6d4a1c2f6b7e8d9a0c3e5b1f4d6e2a3b7c8d9e0f1",
    # Add more device signatures as needed
}

def process_iot_packet(dev_id: str, crypto_sign: str, packet_content: dict):
    """
    Authenticates and processes a data packet from an IoT device.

    Parameters
    ----------
    dev_id : str
        Unique identifier for the IoT device.
    crypto_sign : str
        Cryptographic signature attached to the packet (hex-encoded).
    packet_content : dict
        The actual content of the packet.

    Returns
    -------
    dict | None
        The packet content if authentication succeeds; otherwise, None.

    Raises
    ------
    ConnectionError
        If there is an issue receiving data from the device.
    """
    # Simulate a potential network hiccup
    if random.random() < 0.01:  # 1% chance of failure
        raise ConnectionError(f"Failed to receive data from device {dev_id}")

    # Retrieve the expected signature for this device
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(dev_id)
    if not expected_sig:
        # Unknown device: treat as unauthenticated
        return None

    # Normalize both signatures to lowercase hex strings
    crypto_sign = crypto_sign.lower()
    expected_sig = expected_sig.lower()

    # Use hmac.compare_digest for constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(crypto_sign, expected_sig):
        # Signature mismatch – reject the packet
        return None

    # At this point, the signature is verified; safely return the content
    return packet_content