import hmac
import hashlib
from typing import Dict, Optional

# Global dictionary mapping device IDs to their secret keys (HMAC keys)
TRUSTED_DEVICE_SIGNATURES: Dict[str, bytes] = {
    # Example entries – in a real system these would be securely stored
    "device-001": b"supersecretkey1",
    "device-002": b"supersecretkey2",
}

def _compute_signature(message: bytes, key: bytes) -> str:
    """
    Compute an HMAC-SHA256 signature for the given message using the provided key.
    Returns a hex-encoded string suitable for comparison with the transmitted signature.
    """
    return hmac.new(key, message, hashlib.sha256).hexdigest()

def validate_device_packet(
    iot_device_id: str,
    iot_signature: str,
    iot_data: Optional[Dict]
) -> Optional[Dict]:
    """
    Validate an IoT data packet and return the processed data if authentication succeeds.

    Parameters
    ----------
    iot_device_id : str
        Unique identifier of the sending device.
    iot_signature : str
        Hex-encoded cryptographic signature sent with the packet.
    iot_data : dict | None
        Payload of the data packet.

    Returns
    -------
    dict | None
        The original payload if signature validation passes; otherwise, None.

    Raises
    ------
    ConnectionError
        If the packet could not be received (i.e., ``iot_data`` is None).
    """
    # 1. Ensure we actually received a packet
    if iot_data is None:
        raise ConnectionError(f"Packet from device {iot_device_id} could not be received.")

    # 2. Retrieve the trusted key for this device
    key = TRUSTED_DEVICE_SIGNATURES.get(iot_device_id)
    if key is None:
        # Unknown device – treat as a failed authentication
        return None

    # 3. Serialize the data deterministically for signature verification.
    #    We use JSON with sorted keys to ensure consistent ordering across
    #    different platforms.
    import json
    try:
        serialized = json.dumps(iot_data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    except (TypeError, ValueError):
        # Payload is not JSON‑serializable – reject
        return None

    # 4. Compute the expected signature
    expected_sig = _compute_signature(serialized, key)

    # 5. Compare signatures using a timing‑attack resistant comparison
    if not hmac.compare_digest(expected_sig, iot_signature):
        # Signature mismatch – authentication failed
        return None

    # 6. Authentication succeeded – return the original payload.
    #    In a real implementation, additional processing could be performed here.
    return iot_data