import hashlib
import hmac
from typing import Dict, Optional

# Example trusted signatures dictionary.
# In a real system these would be securely stored and likely be public keys or shared secrets.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # device_id : shared_secret (hex encoded)
    "device_001": "5f2c9b3a7e1d4c6b8f0e2d4c3a9b1e5f",
    "device_002": "7e1d4c6b8f0e2d4c3a9b1e5f5f2c9b3a",
    # Add more devices as needed
}


def _compute_signature(shared_secret: str, payload: Dict) -> str:
    """
    Compute HMAC-SHA256 signature over the JSON-encoded payload.
    The shared secret is expected to be a hex string; it will be decoded
    before use.
    """
    # Convert payload to canonical JSON representation (sorted keys)
    import json
    message = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    secret_bytes = bytes.fromhex(shared_secret)
    return hmac.new(secret_bytes, message, hashlib.sha256).hexdigest()


def handle_data_packet(device_id: str,
                       signature: str,
                       data: Dict) -> Optional[Dict]:
    """
    Verify the cryptographic signature of an IoT data packet and return
    the payload if it is valid.

    Parameters
    ----------
    device_id : str
        Identification number of the IoT device that sent the data.
    signature : str
        Hex-encoded cryptographic signature accompanying the packet.
    data : dict
        The payload of the packet.

    Returns
    -------
    dict or None
        The original data dictionary if signature verification succeeds,
        otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the data packet is missing or not a dictionary.
    """
    # Validate that we received a proper packet
    if data is None or not isinstance(data, dict):
        raise ConnectionError("Data packet not received properly")

    # Retrieve the trusted secret for this device
    shared_secret = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not shared_secret:
        # Unknown device or no trusted secret; reject silently
        return None

    try:
        # Compute expected signature
        expected_sig = _compute_signature(shared_secret, data)
    except (ValueError, TypeError):
        # Any error in computing signature indicates malformed secret or data
        return None

    # Constant‑time comparison to mitigate timing attacks
    if hmac.compare_digest(expected_sig, signature):
        return data

    # Signature did not match
    return None