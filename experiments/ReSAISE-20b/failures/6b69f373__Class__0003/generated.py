import hmac
import hashlib
from typing import Dict, Optional

# Example global mapping of device IDs to shared secrets (HMAC keys)
TRUSTED_DEVICE_SIGNATURES: Dict[str, bytes] = {
    # device_id : secret_key
    "device-001": b"supersecretkey1",
    "device-002": b"anothersecret2",
    # Add more devices as needed
}

def validate_device_packet(
    iot_device_id: str,
    iot_signature: str,
    iot_data: Optional[Dict]
) -> Optional[Dict]:
    """
    Validate an IoT data packet using HMAC-SHA256.

    Parameters
    ----------
    iot_device_id : str
        Unique identifier of the sending IoT device.
    iot_signature : str
        Base64-encoded HMAC signature included with the packet.
    iot_data : dict | None
        The payload of the data packet.

    Returns
    -------
    dict or None
        Returns the original data dictionary if signature validation passes,
        otherwise returns ``None``.
    Raises
    ------
    ConnectionError
        If the packet could not be received (i.e., ``iot_data`` is ``None``).
    """
    # Simulate a failure to receive the packet
    if iot_data is None:
        raise ConnectionError("Failed to receive data from device.")

    # Ensure the device is known
    secret_key = TRUSTED_DEVICE_SIGNATURES.get(iot_device_id)
    if not secret_key:
        # Unknown device – treat as invalid
        return None

    try:
        # Recompute HMAC over the serialized JSON representation of the data.
        # Sorting keys ensures deterministic ordering for signature generation.
        import json
        payload = json.dumps(iot_data, sort_keys=True).encode("utf-8")
    except Exception:
        # Malformed data; treat as invalid
        return None

    # Compute the expected signature
    computed_hmac = hmac.new(secret_key, payload, hashlib.sha256).digest()

    # The incoming signature is expected to be base64-encoded
    import base64
    try:
        received_hmac = base64.b64decode(iot_signature, validate=True)
    except (base64.binascii.Error, ValueError):
        # Malformed signature
        return None

    # Use constant‑time comparison to mitigate timing attacks (CWE‑345)
    if not hmac.compare_digest(computed_hmac, received_hmac):
        return None

    # Signature verified – return the data for further processing
    return iot_data