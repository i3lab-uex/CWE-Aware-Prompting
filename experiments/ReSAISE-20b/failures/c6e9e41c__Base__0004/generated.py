import hmac
import hashlib
from typing import Dict, Optional

# Global mapping of device IDs to their trusted HMAC secret keys (hex strings).
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; in real use these would be securely stored.
    "device_001": "a1b2c3d4e5f67890abcdef1234567890",
    "device_002": "deadbeefcafebabe0123456789abcdef",
}

def _serialize_payload(payload: Dict) -> bytes:
    """
    Serialize the payload deterministically for signing.
    Uses JSON with sorted keys to avoid signature differences due to key order.
    """
    import json
    return json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")

def _hmac_sha256(secret: bytes, message: bytes) -> str:
    """
    Compute the HMAC-SHA256 digest of *message* using *secret*.
    Return a hex-encoded string.
    """
    return hmac.new(secret, message, hashlib.sha256).hexdigest()

def verify_data_packet(device: str, sig: str, payload: Dict) -> Optional[Dict]:
    """
    Validate the cryptographic signature of an incoming IoT data packet.

    Parameters
    ----------
    device : str
        Unique identifier of the sending IoT device.
    sig : str
        Hex-encoded cryptographic signature attached to the packet.
    payload : dict
        The actual data contained in the packet.

    Returns
    -------
    dict | None
        The payload dictionary if signature verification succeeds,
        otherwise None.

    Raises
    ------
    ConnectionError
        If the device is unknown or no trusted signature key is available.
    """
    # 1. Ensure we have a trusted key for this device
    if device not in TRUSTED_DEVICE_SIGNATURES:
        raise ConnectionError(f"Unrecognized device: {device}")

    secret_hex = TRUSTED_DEVICE_SIGNATURES[device]
    try:
        secret_bytes = bytes.fromhex(secret_hex)
    except ValueError as exc:
        raise ConnectionError(f"Invalid secret key format for device {device}") from exc

    # 2. Serialize payload deterministically
    try:
        message = _serialize_payload(payload)
    except Exception as exc:  # pragma: no cover
        raise ConnectionError("Failed to serialize payload") from exc

    # 3. Compute expected HMAC
    expected_sig = _hmac_sha256(secret_bytes, message)

    # 4. Constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(expected_sig, sig.lower()):
        return None

    # 5. Signature verified; return the payload
    return payload