import hashlib
import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their shared secret keys (or expected signatures)
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with real device secrets or signatures
    "device_001": "secret_key_for_device_001",
    "device_002": "secret_key_for_device_002",
}

def _compute_hmac_sha256(secret: str, data: bytes) -> str:
    """
    Compute the HMAC-SHA256 of `data` using the provided secret key.
    Returns the hex digest as a string.
    """
    return hmac.new(secret.encode("utf-8"), data, hashlib.sha256).hexdigest()

def process_iot_packet(dev_id: str,
                       crypto_sign: str,
                       packet_content: Dict) -> Optional[Dict]:
    """
    Authenticate and process a data packet from an IoT device.

    Parameters
    ----------
    dev_id : str
        Unique identifier of the sending IoT device.
    crypto_sign : str
        Cryptographic signature attached to the packet (hex string).
    packet_content : dict
        The actual content of the data packet.

    Returns
    -------
    dict or None
        Returns the packet content if signature verification succeeds,
        otherwise returns ``None``.

    Raises
    ------
    ConnectionError
        If the device is unknown or if packet reception fails.
    """
    # Ensure we have a payload to work with
    if not isinstance(packet_content, dict):
        raise ConnectionError("Invalid packet format received from device.")

    # Verify that the device is known
    secret_key = TRUSTED_DEVICE_SIGNATURES.get(dev_id)
    if secret_key is None:
        raise ConnectionError(f"Unknown device ID: {dev_id}")

    # Prepare the data that was signed.
    # We serialize the packet content in a deterministic way (JSON with sorted keys)
    import json
    try:
        payload_bytes = json.dumps(packet_content, sort_keys=True).encode("utf-8")
    except Exception as exc:
        raise ConnectionError(f"Failed to serialize packet content: {exc}") from exc

    # Compute the expected HMAC
    expected_sign = _compute_hmac_sha256(secret_key, payload_bytes)

    # Constant-time comparison to mitigate timing attacks
    if not hmac.compare_digest(expected_sign, crypto_sign):
        # Signature does not match – treat as untrusted data
        return None

    # Signature verified; return the packet content
    return packet_content