import json
import hmac
import hashlib
from typing import Dict, Any

# Global mapping of device IDs to their shared secret keys (hex-encoded)
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (replace with real secrets)
    "device-001": "a1b2c3d4e5f60718293a4b5c6d7e8f90",
    "device-002": "0f9e8d7c6b5a4e3d2c1b0a9988776655",
    # Add more devices as needed
}


def process_iot_packet(dev_id: str, crypto_sign: str, packet_content: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Validate and process an IoT data packet.

    Parameters
    ----------
    dev_id : str
        Unique identifier of the sending device.
    crypto_sign : str
        Hex-encoded HMAC SHA256 signature that accompanies the packet.
    packet_content : dict
        The actual data payload of the packet.

    Returns
    -------
    dict | None
        The original packet content if signature verification succeeds;
        otherwise, None.

    Raises
    ------
    ConnectionError
        If the device is unknown or a communication error occurs.
    """
    # 1. Verify that the device is trusted
    if dev_id not in TRUSTED_DEVICE_SIGNATURES:
        raise ConnectionError(f"Unknown device ID: {dev_id}")

    # 2. Prepare the message for signing
    try:
        # Canonical JSON representation ensures consistent ordering and spacing.
        serialized = json.dumps(packet_content, separators=(",", ":"), sort_keys=True).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ConnectionError(f"Failed to serialize packet content: {exc}") from exc

    # 3. Compute the expected HMAC using the device's secret key
    try:
        secret_key = bytes.fromhex(TRUSTED_DEVICE_SIGNATURES[dev_id])
    except ValueError as exc:
        raise ConnectionError(f"Invalid secret key format for device {dev_id}") from exc

    expected_mac = hmac.new(secret_key, serialized, hashlib.sha256).hexdigest()

    # 4. Constant‑time comparison to prevent timing attacks (CWE‑693)
    if not hmac.compare_digest(expected_mac, crypto_sign.lower()):
        return None

    # 5. Signature is valid – return the original content
    return packet_content