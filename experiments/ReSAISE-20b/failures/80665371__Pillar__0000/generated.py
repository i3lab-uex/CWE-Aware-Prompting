import hmac
import hashlib
from typing import Dict, Optional

# Global dictionary mapping device IDs to their trusted HMAC secret keys.
TRUSTED_DEVICE_SIGNATURES: Dict[str, bytes] = {
    # Example entries – replace with actual device secrets.
    "device_001": b"super_secret_key_for_device_001",
    "device_002": b"another_super_secret_key_for_device_002",
}

def process_data_packet(dev_id: str, sign: str, payload: Dict) -> Optional[Dict]:
    """
    Validate and process an incoming data packet from an IoT device.

    Parameters
    ----------
    dev_id : str
        Unique identifier of the IoT device that sent the packet.
    sign : str
        Cryptographic signature attached to the packet (hex-encoded).
    payload : dict
        The actual data or payload to be processed.

    Returns
    -------
    dict | None
        The original payload if the signature is verified successfully;
        otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the device ID is unknown or there was an error retrieving the
        trusted signature.
    """
    # Ensure the device is known and has a registered secret key.
    try:
        secret = TRUSTED_DEVICE_SIGNATURES[dev_id]
    except KeyError as exc:
        raise ConnectionError(f"Unknown device ID: {dev_id}") from exc

    # Compute the expected HMAC-SHA256 signature over the JSON representation
    # of the payload.  Using a deterministic encoding ensures reproducibility.
    try:
        import json
        message = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    except Exception as exc:
        raise ConnectionError(f"Failed to encode payload for device {dev_id}") from exc

    expected_hmac = hmac.new(secret, message, hashlib.sha256).hexdigest()

    # Use constant‑time comparison to mitigate timing attacks.
    if not hmac.compare_digest(expected_hmac, sign):
        return None

    # Signature verified – safely return the payload.
    return payload