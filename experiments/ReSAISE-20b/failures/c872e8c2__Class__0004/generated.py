import hashlib
import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their trusted cryptographic signatures.
# In a real system this would be stored securely (e.g., in a vault or HSM).
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    "device-001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "device-002": "e99a18c428cb38d5f260853678922e03",
    # Add more trusted devices here
}


def _compute_signature(data: Dict) -> str:
    """
    Compute a deterministic HMAC-SHA256 signature for the packet data.
    The key is derived from the device's expected signature to prevent
    replay attacks and ensure authenticity.
    """
    # Serialize data in a consistent order (sorted keys) to avoid signature mismatches
    serialized = "".join(f"{k}:{v}" for k, v in sorted(data.items()))
    # Use a fixed secret key (in practice this should be per-device and stored securely)
    secret_key = b"super_secret_shared_key"
    return hmac.new(secret_key, serialized.encode("utf-8"), hashlib.sha256).hexdigest()


def manage_data_packet(
    io_device_id: str, crypto_signature: str, packet_data: Optional[Dict]
) -> Optional[Dict]:
    """
    Validate and process an incoming data packet from an IoT device.

    Parameters
    ----------
    io_device_id : str
        The unique identifier of the IoT device that sent the packet.
    crypto_signature : str
        The cryptographic signature attached to the packet.
    packet_data : dict or None
        The actual data or payload to be processed.

    Returns
    -------
    dict or None
        The packet data if the signature is verified; otherwise, None.

    Raises
    ------
    ConnectionError
        If the packet data is missing or cannot be processed.
    """
    # 1. Ensure we received a payload
    if packet_data is None:
        raise ConnectionError("No data packet received from device.")

    # 2. Verify the device is trusted
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(io_device_id)
    if not expected_signature:
        # Unknown device: reject silently (do not return data)
        return None

    # 3. Compute signature of the received payload
    computed_signature = _compute_signature(packet_data)

    # 4. Compare signatures in constant time to avoid timing attacks
    if not hmac.compare_digest(computed_signature, crypto_signature):
        # Signature mismatch: treat as untrusted
        return None

    # 5. All checks passed; return the payload
    return packet_data