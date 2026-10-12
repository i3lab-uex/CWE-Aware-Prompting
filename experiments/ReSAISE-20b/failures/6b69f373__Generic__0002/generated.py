import hmac
import hashlib
from typing import Dict, Optional

# Example trusted signatures mapping (device_id -> secret key in hex)
TRUSTED_DEVICE_SIGNATURES: Dict[str, bytes] = {
    "device-001": b"0123456789abcdef",
    "device-002": b"fedcba9876543210",
    # Add more device keys as needed
}


def _compute_hmac(secret: bytes, data: Dict) -> str:
    """
    Compute HMAC-SHA256 of the canonical JSON representation of *data*
    using *secret* as the key.
    """
    # Canonical JSON: sorted keys, no whitespace
    json_bytes = (
        "{"
        + ",".join(
            f'"{k}":{repr(v)}' for k, v in sorted(data.items())
        )
        + "}"
    ).encode("utf-8")
    digest = hmac.new(secret, json_bytes, hashlib.sha256).hexdigest()
    return digest


def validate_device_packet(
    iot_device_id: str,
    iot_signature: str,
    iot_data: Dict,
) -> Optional[Dict]:
    """
    Validate the signature of an IoT data packet and return the processed
    payload if verification succeeds.

    Parameters
    ----------
    iot_device_id : str
        Unique identifier of the device sending the packet.
    iot_signature : str
        Hexadecimal signature provided by the device.
    iot_data : dict
        The payload of the packet.

    Returns
    -------
    dict | None
        Processed data if signature verification succeeds; otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the packet could not be received (e.g., missing data).
    """
    # Simulate packet reception failure
    if iot_data is None:
        raise ConnectionError("Failed to receive data packet from device.")

    # Ensure the device is known
    if iot_device_id not in TRUSTED_DEVICE_SIGNATURES:
        return None

    secret_key = TRUSTED_DEVICE_SIGNATURES[iot_device_id]

    # Compute expected signature
    expected_sig = _compute_hmac(secret_key, iot_data)

    # Constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(expected_sig, iot_signature):
        return None

    # At this point the packet is authenticated; perform any additional
    # processing required by your application.
    # For demonstration, we simply return the data unchanged.
    return iot_data