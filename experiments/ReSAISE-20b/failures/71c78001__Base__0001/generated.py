import hmac
import hashlib
from typing import Dict, Optional

# Global mapping from device ID to its shared secret (HMAC key)
TRUSTED_DEVICE_SIGNATURES: Dict[str, bytes] = {
    # Example entries; in production these would be securely stored
    "device_001": b"supersecretkey1",
    "device_002": b"anotherverylongsecretkey2",
}

def _verify_signature(dev_id: str, crypto_sign: bytes, packet_content: dict) -> bool:
    """
    Verify the HMAC-SHA256 signature of the packet_content.
    The signature is expected to be a hex-encoded string.
    """
    if dev_id not in TRUSTED_DEVICE_SIGNATURES:
        return False

    key = TRUSTED_DEVICE_SIGNATURES[dev_id]
    # Serialize packet_content deterministically
    message = _serialize_packet(packet_content)
    computed_hmac = hmac.new(key, message.encode("utf-8"), hashlib.sha256).hexdigest()

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(computed_hmac, crypto_sign.lower())

def _serialize_packet(packet: dict) -> str:
    """
    Serialize the packet to a JSON string with sorted keys for deterministic output.
    """
    import json
    return json.dumps(packet, separators=(",", ":"), sort_keys=True)

def process_iot_packet(dev_id: str, crypto_sign: str, packet_content: dict) -> Optional[Dict]:
    """
    Authenticate and process a data packet from an IoT device.

    Parameters
    ----------
    dev_id : str
        Unique identifier for the IoT device.
    crypto_sign : str
        Hex‑encoded cryptographic signature attached to the packet.
    packet_content : dict
        The actual data payload.

    Returns
    -------
    Optional[Dict]
        The packet content if the signature is valid, otherwise None.

    Raises
    ------
    ConnectionError
        If there was an issue receiving data from the IoT device.
    """
    # Simulate potential I/O error (in real code this would be a network read)
    if packet_content is None:
        raise ConnectionError("Failed to receive data from device")

    # Validate signature
    try:
        valid = _verify_signature(dev_id, crypto_sign.encode("utf-8"), packet_content)
    except Exception:
        # Any unexpected error during verification is treated as invalid
        return None

    if not valid:
        return None

    # At this point, the packet is authenticated; further processing can occur
    return packet_content