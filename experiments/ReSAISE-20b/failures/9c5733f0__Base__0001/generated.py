import hmac
import hashlib
import json
from typing import Dict, Optional

# Global mapping of device IDs to their shared secret keys (hex‑encoded)
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with real secrets
    "device_001": "a1b2c3d4e5f678901234567890abcdef",
    "device_002": "fedcba09876543211234567890abcdef",
}

def _compute_signature(secret_key: bytes, data: dict) -> str:
    """
    Compute an HMAC‑SHA256 signature over the JSON representation of *data*.
    The JSON string is deterministic (sorted keys, no whitespace).
    """
    json_bytes = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hmac.new(secret_key, json_bytes, hashlib.sha256).hexdigest()

def process_packet_data(
    id_device: str,
    packet_signature: str,
    packet_data: Dict
) -> Optional[Dict]:
    """
    Authenticate and process a data packet from an IoT device.

    Parameters
    ----------
    id_device : str
        Unique identifier of the sending device.
    packet_signature : str
        Hex‑encoded cryptographic signature provided with the packet.
    packet_data : dict
        The actual payload of the packet.

    Returns
    -------
    dict or None
        The original *packet_data* if the signature is valid; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the packet data is not a dictionary (simulating a bad reception).
    """
    # Simulate a failure in receiving data
    if not isinstance(packet_data, dict):
        raise ConnectionError("Failed to receive valid packet data from device.")

    # Retrieve the secret key for this device
    hex_key = TRUSTED_DEVICE_SIGNATURES.get(id_device)
    if not hex_key:
        # Unknown device – reject silently
        return None

    try:
        secret = bytes.fromhex(hex_key)
    except ValueError:
        # Malformed key – treat as authentication failure
        return None

    # Compute the expected signature in a constant‑time manner
    try:
        expected_sig = _compute_signature(secret, packet_data)
    except Exception:
        # Any error in signing is treated as a failure
        return None

    if not hmac.compare_digest(expected_sig, packet_signature):
        # Signature does not match
        return None

    # All checks passed – return the payload as trusted data
    return packet_data