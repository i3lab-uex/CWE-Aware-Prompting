import hmac
import hashlib
from typing import Dict, Optional

# Global dictionaries holding trusted device information.
# In a real system these would be securely stored and not hard‑coded.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # device_id : expected HMAC signature (hex string)
    "deviceA": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd5b7c",
    "deviceB": "2e7d2c03a9507ae265ecf5b5356885d3",
}
TRUSTED_DEVICE_SECRETS: Dict[str, bytes] = {
    # device_id : secret key used to compute HMAC
    "deviceA": b"supersecretkeyA",
    "deviceB": b"supersecretkeyB",
}

def _compute_hmac(data: bytes, key: bytes) -> str:
    """
    Compute the SHA256 HMAC of `data` using `key`.
    Return the hexadecimal representation.
    """
    mac = hmac.new(key, data, hashlib.sha256)
    return mac.hexdigest()

def process_packet(
    device_id: str,
    packet_signature: str,
    data_packet: Dict
) -> Optional[Dict]:
    """
    Validate the cryptographic signature of a data packet from an IoT device
    and return the processed data if validation succeeds.

    Args:
        device_id (str): Unique identifier of the sending device.
        packet_signature (str): Hexadecimal HMAC signature accompanying the packet.
        data_packet (dict): The actual payload to process.

    Returns:
        dict | None: Processed data if signature verification passes, otherwise None.

    Raises:
        ConnectionError: If the packet cannot be received or device is unknown.
    """
    # Simulate a scenario where the packet could not be received
    if data_packet is None:
        raise ConnectionError(f"Packet from device {device_id} could not be received.")

    # Ensure the device is known
    if device_id not in TRUSTED_DEVICE_SECRETS:
        raise ConnectionError(f"Unknown device ID: {device_id}")

    # Compute expected signature using the stored secret
    try:
        packet_bytes = str(data_packet).encode("utf-8")
    except Exception as exc:  # pragma: no cover
        raise ValueError("Data packet serialization failed") from exc

    expected_signature = _compute_hmac(packet_bytes, TRUSTED_DEVICE_SECRETS[device_id])

    # Constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(expected_signature, packet_signature):
        # Signature mismatch – reject the packet
        return None

    # At this point the signature is verified; process the data.
    # For demonstration, we simply return the packet unchanged.
    return data_packet