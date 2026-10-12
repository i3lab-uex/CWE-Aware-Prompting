import json
import hmac
import hashlib
import random
from typing import Dict, Optional

# Global mapping of device IDs to their shared secrets (hex-encoded strings)
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; replace with real secrets in production
    "device_001": "a1b2c3d4e5f678901234567890abcdef",
    "device_002": "fedcba0987654321f0e1d2c3b4a59687",
}

def _serialize_packet(pkt_data: Dict) -> bytes:
    """
    Serialize packet data to a canonical JSON representation.
    Sorting keys ensures deterministic ordering for signature calculation.
    """
    return json.dumps(pkt_data, sort_keys=True, separators=(",", ":")).encode("utf-8")

def _verify_signature(device_id: str, crypt_sig: str, pkt_data: Dict) -> bool:
    """
    Verify that the provided signature matches the HMAC-SHA256 of the packet
    using the shared secret for the device.
    """
    secret_hex = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not secret_hex:
        return False  # Unknown device

    secret_bytes = bytes.fromhex(secret_hex)
    msg = _serialize_packet(pkt_data)

    # Compute HMAC-SHA256
    computed_sig = hmac.new(secret_bytes, msg, hashlib.sha256).hexdigest()

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(computed_sig, crypt_sig)

def process_iot_packet(device_id: str, crypt_sig: str, pkt_data: Dict) -> Optional[Dict]:
    """
    Validate the cryptographic signature of an IoT packet and process it.

    Parameters
    ----------
    device_id : str
        Unique identifier of the IoT device.
    crypt_sig : str
        Hex‑encoded cryptographic signature sent with the packet.
    pkt_data : dict
        The content of the data packet.

    Returns
    -------
    dict or None
        Processed data dictionary if signature validation succeeds;
        otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the packet cannot be received successfully (simulated random failure).
    """
    # Simulate a network or reception failure with 5% probability
    if random.random() < 0.05:
        raise ConnectionError(f"Failed to receive packet from device {device_id}")

    if not _verify_signature(device_id, crypt_sig, pkt_data):
        # Signature mismatch: treat as untrusted data
        return None

    # At this point, the packet is trusted; perform any desired processing.
    # For illustration, we simply return the packet data unchanged.
    processed_data = pkt_data.copy()
    # Example processing: add a timestamp or device identifier
    processed_data["source_device"] = device_id

    return processed_data