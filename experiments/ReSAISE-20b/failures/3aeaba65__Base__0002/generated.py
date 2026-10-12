import hashlib
import hmac
from typing import Dict, Optional

# Example trusted device signatures.
# In a real system this would be stored securely (e.g., in a vault).
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    "device_001": "4b65792d736563726574",  # hex‑encoded secret
    "device_002": "5f6172746963652d73656372",
    # Add more devices as needed
}

def verify_iot_signature(
    iot_id: str,
    crypto_signature: str,
    packet_info: Dict
) -> Optional[Dict]:
    """
    Validate the cryptographic signature of an IoT data packet.

    Parameters
    ----------
    iot_id : str
        Unique identifier of the IoT device.
    crypto_signature : str
        Hex‑encoded HMAC-SHA256 signature received with the packet.
    packet_info : dict
        The data payload to be processed.

    Returns
    -------
    dict | None
        The packet_info dictionary if the signature is valid,
        otherwise None.

    Raises
    ------
    ConnectionError
        If the packet cannot be retrieved from the device (simulated).
    """
    # Simulate a potential communication failure
    if iot_id not in TRUSTED_DEVICE_SIGNATURES:
        raise ConnectionError(f"Device {iot_id} is unknown or unreachable")

    # Retrieve the shared secret for this device
    secret_hex = TRUSTED_DEVICE_SIGNATURES[iot_id]
    try:
        secret_bytes = bytes.fromhex(secret_hex)
    except ValueError as exc:
        raise ConnectionError(f"Invalid secret format for device {iot_id}") from exc

    # Recreate the expected HMAC over the packet payload
    # For simplicity, we serialize the dict in a deterministic way.
    # In production use a proper serialization format (e.g., JSON with sorted keys).
    payload_bytes = str(packet_info).encode("utf-8")
    expected_hmac = hmac.new(secret_bytes, payload_bytes, hashlib.sha256).hexdigest()

    # Constant‑time comparison to prevent timing attacks
    if hmac.compare_digest(expected_hmac, crypto_signature):
        return packet_info
    else:
        return None