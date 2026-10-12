import hmac
import hashlib
from typing import Dict, Optional

# Global dictionary mapping device IDs to their secret keys (used for HMAC verification)
TRUSTED_DEVICE_SIGNATURES: Dict[str, bytes] = {
    # Example entries – replace with real secrets in production
    "device_a": b"super_secret_key_1",
    "device_b": b"super_secret_key_2",
}

def _compute_hmac(secret: bytes, data: bytes) -> str:
    """
    Compute a base64-encoded HMAC-SHA256 digest for the given data using the supplied secret.
    """
    mac = hmac.new(secret, msg=data, digestmod=hashlib.sha256)
    return mac.hexdigest()

def process_iot_packet(
    dev_id: str,
    crypto_sign: str,
    packet_content: Dict
) -> Optional[Dict]:
    """
    Authenticate and process an IoT data packet.

    Parameters
    ----------
    dev_id : str
        Unique identifier of the IoT device.
    crypto_sign : str
        Hex-encoded cryptographic signature (HMAC-SHA256) sent by the device.
    packet_content : dict
        The payload of the packet.

    Returns
    -------
    dict | None
        The original packet content if authentication succeeds; otherwise, None.

    Raises
    ------
    ConnectionError
        If packet_content is missing or cannot be processed (simulating a reception error).
    """
    # 1. Validate input
    if packet_content is None:
        raise ConnectionError("Failed to receive data from device.")

    # 2. Retrieve the secret key for this device
    secret_key = TRUSTED_DEVICE_SIGNATURES.get(dev_id)
    if not secret_key:
        # Unknown device – treat as authentication failure
        return None

    try:
        # 3. Serialize the packet content deterministically (JSON with sorted keys)
        import json
        payload_bytes = json.dumps(packet_content, sort_keys=True).encode("utf-8")
    except Exception as exc:
        # If serialization fails, treat it as a reception error
        raise ConnectionError("Error processing packet content.") from exc

    # 4. Compute expected HMAC
    expected_sign = _compute_hmac(secret_key, payload_bytes)

    # 5. Constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(expected_sign, crypto_sign):
        # Signature mismatch – authentication failed
        return None

    # 6. Authentication succeeded; return the original packet content
    return packet_content