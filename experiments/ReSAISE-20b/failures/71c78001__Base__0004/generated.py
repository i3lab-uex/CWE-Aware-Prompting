import hmac
import hashlib
from typing import Dict, Optional

# Global mapping of device IDs to their shared secret keys (hex strings).
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries – in real usage these would be securely stored and rotated.
    "device_001": "4a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef",
    "device_002": "a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef01",
}


def _validate_signature(dev_id: str, crypto_sign: str, packet_content: Dict) -> bool:
    """
    Validate the cryptographic signature using HMAC-SHA256.

    Parameters
    ----------
    dev_id : str
        Identifier of the device.
    crypto_sign : str
        Signature received from the device, expected to be a hex string.
    packet_content : dict
        The payload of the packet (must be serialized deterministically).

    Returns
    -------
    bool
        True if signature is valid, False otherwise.
    """
    secret_hex = TRUSTED_DEVICE_SIGNATURES.get(dev_id)
    if not secret_hex:
        return False

    # Serialize packet content deterministically (JSON with sorted keys)
    import json
    message = json.dumps(packet_content, separators=(",", ":"), sort_keys=True).encode("utf-8")

    # Compute HMAC-SHA256 over the message using the secret key
    try:
        secret = bytes.fromhex(secret_hex)
    except ValueError:
        # Secret not a valid hex string
        return False

    expected_sig = hmac.new(secret, message, hashlib.sha256).hexdigest()

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sig, crypto_sign.lower())


def process_iot_packet(dev_id: str, crypto_sign: str, packet_content: Dict) -> Optional[Dict]:
    """
    Authenticate and process an IoT data packet.

    Parameters
    ----------
    dev_id : str
        Unique identifier of the IoT device.
    crypto_sign : str
        Cryptographic signature attached to the packet (hex string).
    packet_content : dict
        Payload of the packet.

    Returns
    -------
    dict | None
        The packet content if authentication succeeds; otherwise, None.

    Raises
    ------
    ConnectionError
        If the packet could not be received (simulated here as an empty content).
    """
    # Simulate a receive error: in real code this would be part of the I/O layer
    if packet_content is None:
        raise ConnectionError(f"Failed to receive data from device {dev_id}")

    if not _validate_signature(dev_id, crypto_sign, packet_content):
        return None

    # At this point the signature is verified; safely return the payload
    return packet_content