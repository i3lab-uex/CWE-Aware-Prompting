import json
import hashlib
from typing import Dict, Optional

# Global mapping of device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; in production these would be securely stored.
    "device-001": "a3f1c8e2b4d5... (hex digest)",
    "device-002": "7c9e2f3a1b4d... (hex digest)",
    # ...
}

def _compute_signature(packet: Dict) -> str:
    """
    Compute a SHA‑256 hex digest of the JSON representation of *packet*.
    The packet is sorted by keys to ensure deterministic serialization.
    """
    json_str = json.dumps(packet, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(json_str.encode("utf-8")).hexdigest()

def verify_iot_signature(
    iot_id: str,
    crypto_signature: str,
    packet_info: Dict
) -> Optional[Dict]:
    """
    Verify that the supplied *crypto_signature* matches the expected
    signature for the given IoT device and packet content.

    Parameters:
        iot_id (str): Unique identifier for the IoT device.
        crypto_signature (str): Signature attached to the data packet.
        packet_info (dict): The actual content of the packet.

    Returns:
        dict: The original packet data if the signature is valid.
        None: If the signature does not match or the device ID is unknown.

    Raises:
        ConnectionError: If packet_info lacks required keys indicating a
                         communication problem.
    """
    # Basic sanity check: ensure packet contains expected structure.
    if not isinstance(packet_info, dict) or "payload" not in packet_info:
        raise ConnectionError("Invalid or incomplete packet received from device.")

    # Retrieve the trusted signature for this device.
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(iot_id)
    if expected_sig is None:
        # Unknown device: treat as invalid.
        return None

    # Compute the signature of the incoming packet.
    computed_sig = _compute_signature(packet_info)

    # Constant‑time comparison to mitigate timing attacks.
    if hashlib.compare_digest(computed_sig, expected_sig) and \
       hashlib.compare_digest(crypto_signature, computed_sig):
        return packet_info

    # Signature mismatch: reject data.
    return None