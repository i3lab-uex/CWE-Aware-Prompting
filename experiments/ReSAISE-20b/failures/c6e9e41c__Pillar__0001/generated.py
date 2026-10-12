import hmac
import hashlib
from typing import Dict, Optional

# Global mapping of device ID to its trusted HMAC key (hex‑encoded string)
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (replace with real keys)
    "device_001": "a1b2c3d4e5f60718293a4b5c6d7e8f901234567890abcdef1234567890abcdef",
    "device_002": "b2c3d4e5f60718293a4b5c6d7e8f901234567890abcdef1234567890abcdefa1",
}

def _hmac_sha256(key: bytes, message: bytes) -> bytes:
    """
    Return the HMAC‑SHA256 digest of *message* using *key*.
    """
    return hmac.new(key, message, hashlib.sha256).digest()

def verify_data_packet(device: str, sig: str, payload: Dict) -> Optional[Dict]:
    """
    Verify the cryptographic signature of an IoT data packet and return
    the payload if the verification succeeds.

    Parameters
    ----------
    device : str
        Unique identifier of the sending IoT device.
    sig : str
        Hex‑encoded signature attached to the packet.
    payload : dict
        The data or payload to be processed.

    Returns
    -------
    dict | None
        The original payload if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the packet cannot be received or processed (e.g. missing fields).
    """
    # Basic sanity checks
    if not isinstance(device, str) or not device:
        raise ConnectionError("Invalid or missing device identifier.")
    if not isinstance(sig, str) or not sig:
        raise ConnectionError("Missing signature.")
    if not isinstance(payload, dict):
        raise ConnectionError("Payload must be a dictionary.")

    # Retrieve the trusted key for this device
    try:
        key_hex = TRUSTED_DEVICE_SIGNATURES[device]
    except KeyError as exc:
        raise ConnectionError(f"Unknown device ID: {device}") from exc

    try:
        key_bytes = bytes.fromhex(key_hex)
    except ValueError as exc:
        raise ConnectionError("Trusted key is not valid hex.") from exc

    # Serialize the payload deterministically (JSON with sorted keys)
    import json
    try:
        payload_bytes = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ConnectionError("Failed to serialize payload.") from exc

    # Compute expected HMAC
    try:
        expected_sig = _hmac_sha256(key_bytes, payload_bytes).hex()
    except Exception as exc:
        raise ConnectionError("Failed to compute HMAC.") from exc

    # Constant‑time comparison to prevent timing attacks
    if not hmac.compare_digest(expected_sig, sig.lower()):
        return None

    # Signature verified – return the original payload
    return payload