import hmac
import hashlib
from typing import Dict, Optional

# Global dictionary mapping device IDs to their trusted HMAC keys (hex strings)
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (replace with real keys)
    "device001": "a1b2c3d4e5f60718293a4b5c6d7e8f901234567890abcdef1234567890abcdef",
    "device002": "fedcba0987654321f0e1d2c3b4a59687766554433221100ffeeddccbbaa9988",
    # Add more devices as needed
}


def _verify_signature(device_id: str, data: Dict, signature_hex: str) -> bool:
    """
    Verify the HMAC-SHA256 signature of `data` using the key stored in
    TRUSTED_DEVICE_SIGNATURES for the given device_id.
    """
    if device_id not in TRUSTED_DEVICE_SIGNATURES:
        return False

    # Retrieve the key and decode from hex
    key_bytes = bytes.fromhex(TRUSTED_DEVICE_SIGNATURES[device_id])

    # Convert the data dict to a canonical byte representation
    # Here we use JSON with sorted keys for determinism.
    import json

    data_bytes = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")

    # Compute the HMAC
    expected_hmac = hmac.new(key_bytes, data_bytes, hashlib.sha256).hexdigest()

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(expected_hmac, signature_hex.lower())


def handle_data_packet(device_id: str, signature: str, data: Dict) -> Optional[Dict]:
    """
    Process a data packet from an IoT device.

    Parameters
    ----------
    device_id : str
        The identification number of the IoT device that sent the data.
    signature : str
        Hex‑encoded cryptographic signature accompanying the packet.
    data : dict
        The payload of the packet that needs to be processed.

    Returns
    -------
    dict or None
        The original data dictionary if the signature is valid, otherwise `None`.

    Raises
    ------
    ConnectionError
        If the packet is missing required fields or cannot be parsed.
    """
    # Basic sanity checks
    if not isinstance(device_id, str) or not device_id:
        raise ConnectionError("Invalid or missing device ID")

    if not isinstance(signature, str) or not signature:
        raise ConnectionError("Missing cryptographic signature")

    if not isinstance(data, dict):
        raise ConnectionError("Payload must be a dictionary")

    # Verify the signature
    if _verify_signature(device_id, data, signature):
        return data

    # Signature failed
    return None