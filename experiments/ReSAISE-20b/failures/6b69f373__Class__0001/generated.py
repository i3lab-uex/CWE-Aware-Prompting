import hmac
import hashlib
from typing import Dict, Optional

# Global dictionary containing the trusted signatures for each device.
# In a real deployment this would be populated from a secure source
# (e.g. an HSM, a signed manifest file, etc.).
TRUSTED_DEVICE_SIGNATURES: Dict[str, bytes] = {
    # Example entries (device_id -> HMAC secret key)
    "device-001": b"supersecretkey1",
    "device-002": b"anotherverysecretkey2",
}

def validate_device_packet(
    iot_device_id: str,
    iot_signature: str,
    iot_data: Dict
) -> Optional[Dict]:
    """
    Validate and process a data packet from an IoT device.

    Parameters
    ----------
    iot_device_id : str
        Unique identifier of the IoT device.
    iot_signature : str
        Hex-encoded HMAC signature sent with the packet.
    iot_data : dict
        Payload of the data packet.

    Returns
    -------
    dict | None
        The original payload if authentication succeeds; otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the device is not recognized or its signature cannot be verified.
    """
    # 1. Ensure we have a known device
    if iot_device_id not in TRUSTED_DEVICE_SIGNATURES:
        raise ConnectionError(f"Unknown device ID: {iot_device_id}")

    # 2. Retrieve the shared secret key for this device
    secret_key = TRUSTED_DEVICE_SIGNATURES[iot_device_id]

    # 3. Compute the expected HMAC over the serialized payload
    #    We use JSON encoding with sorted keys to ensure deterministic ordering.
    import json
    payload_bytes = json.dumps(iot_data, sort_keys=True).encode("utf-8")
    expected_hmac = hmac.new(secret_key, payload_bytes, hashlib.sha256).hexdigest()

    # 4. Perform a constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(expected_hmac, iot_signature):
        # Authentication failed – do not expose details to the caller
        return None

    # 5. Authentication succeeded; process and return the data
    #    (In this simplified example we simply return the payload unchanged.)
    return iot_data