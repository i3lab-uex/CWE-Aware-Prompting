import hmac
import hashlib
from typing import Dict, Optional

# Global mapping of device IDs to their shared secret keys (hex-encoded).
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (replace with real secrets)
    "device_001": "a1b2c3d4e5f60718293a4b5c6d7e8f901234567890abcdef1234567890abcdef",
    "device_002": "fedcba0987654321efcdab9876543210f123456789abcdef0123456789abcdef",
    # Add more device IDs and their secrets as needed
}


def _compute_hmac(secret_hex: str, data: dict) -> bytes:
    """
    Compute HMAC-SHA256 over the canonical JSON representation of `data`.
    The secret is provided as a hex string.
    """
    # Canonicalize data by sorting keys and encoding to UTF-8 JSON
    import json

    canonical_json = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    secret_bytes = bytes.fromhex(secret_hex)
    return hmac.new(secret_bytes, canonical_json, hashlib.sha256).digest()


def handle_data_packet(device_id: str, signature: str, data: dict) -> Optional[Dict]:
    """
    Verify the cryptographic signature of a data packet from an IoT device.

    Parameters
    ----------
    device_id : str
        Identifier of the sending device.
    signature : str
        Hex-encoded signature that accompanies the packet.
    data : dict
        Payload of the packet.

    Returns
    -------
    dict or None
        The original data dictionary if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the packet is malformed (e.g., missing data or signature).
    """
    # Basic sanity checks
    if not isinstance(device_id, str) or not device_id:
        raise ConnectionError("Malformed packet: missing or invalid device ID.")
    if not isinstance(signature, str) or not signature:
        raise ConnectionError("Malformed packet: missing or invalid signature.")
    if data is None or not isinstance(data, dict):
        raise ConnectionError("Malformed packet: missing or invalid data payload.")

    # Retrieve the shared secret for this device
    secret_hex = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not secret_hex:
        # Unknown device; treat as untrusted
        return None

    try:
        # Compute expected HMAC
        expected_hmac = _compute_hmac(secret_hex, data)
    except Exception:
        # Any failure in HMAC computation is treated as a verification failure
        return None

    try:
        # Convert provided signature from hex to bytes
        provided_hmac = bytes.fromhex(signature)
    except ValueError:
        # Signature is not valid hex
        return None

    # Constant‑time comparison to mitigate timing attacks
    if hmac.compare_digest(expected_hmac, provided_hmac):
        return data

    # Signature mismatch
    return None