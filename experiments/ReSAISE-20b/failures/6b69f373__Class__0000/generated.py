import json
import hmac
import hashlib
from typing import Dict, Optional

# Global mapping of device IDs to their secret keys used for HMAC verification
TRUSTED_DEVICE_SIGNATURES: Dict[str, bytes] = {
    # Example entries – replace with actual device secrets
    "device_001": b"super_secret_key_for_device_001",
    "device_002": b"another_secret_key_for_device_002",
}

def _canonicalize(data: Dict) -> bytes:
    """
    Convert a dictionary to a canonical JSON byte string.
    Sorting keys ensures deterministic serialization for HMAC.
    """
    return json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")

def _verify_signature(device_id: str, signature_hex: str, data_bytes: bytes) -> bool:
    """
    Verify that the provided hex signature matches the HMAC-SHA256
    computed over `data_bytes` using the device's secret key.
    """
    if device_id not in TRUSTED_DEVICE_SIGNATURES:
        return False

    secret = TRUSTED_DEVICE_SIGNATURES[device_id]
    computed_hmac = hmac.new(secret, data_bytes, hashlib.sha256).hexdigest()

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(computed_hmac, signature_hex)

def validate_device_packet(
    iot_device_id: str,
    iot_signature: str,
    iot_data: Optional[Dict]
) -> Optional[Dict]:
    """
    Validate the authenticity of an IoT data packet and return processed data.

    Parameters
    ----------
    iot_device_id : str
        Unique identifier of the sending IoT device.
    iot_signature : str
        Hex‑encoded HMAC signature accompanying the packet.
    iot_data : dict or None
        Payload of the data packet.

    Returns
    -------
    dict | None
        The original payload if signature validation succeeds; otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the packet payload is missing or cannot be processed.
    """
    # Simulate a scenario where the packet could not be received
    if iot_data is None:
        raise ConnectionError(f"Failed to receive data from device {iot_device_id}")

    # Ensure payload is a dictionary
    if not isinstance(iot_data, dict):
        raise ValueError("Packet payload must be a dictionary")

    # Canonicalize the data for HMAC verification
    try:
        payload_bytes = _canonicalize(iot_data)
    except (TypeError, ValueError) as exc:
        # Payload contains non‑serializable data
        raise ValueError(f"Invalid payload structure: {exc}") from exc

    # Verify the signature
    if not _verify_signature(iot_device_id, iot_signature.lower(), payload_bytes):
        # Signature mismatch – treat as untrusted
        return None

    # If validation passes, return the original data (or perform any needed processing)
    return iot_data