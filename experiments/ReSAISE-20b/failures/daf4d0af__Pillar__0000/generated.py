import hmac
import hashlib
from typing import Dict, Optional

# Global mapping of device IDs to their trusted signatures (hex-encoded)
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (replace with real values)
    "device_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "device_002": "e99a18c428cb38d5f260853678922e03",
    # Add more trusted device signatures here
}

def _compute_signature(data: Dict) -> str:
    """
    Compute a deterministic HMAC-SHA256 signature of the data dictionary.
    The data is first serialized into a sorted JSON string to ensure
    consistent ordering across invocations.
    """
    import json

    # Sort keys to guarantee deterministic output
    serialized = json.dumps(data, sort_keys=True, separators=(",", ":"))
    # Use a static secret key for HMAC; in production this should be securely stored
    secret_key = b"super_secret_shared_key"
    return hmac.new(secret_key, serialized.encode("utf-8"), hashlib.sha256).hexdigest()

def handle_data_packet(device_id: str, signature: str, data: Optional[Dict]) -> Optional[Dict]:
    """
    Validate an IoT data packet.

    Parameters
    ----------
    device_id : str
        Identifier of the sending device.
    signature : str
        Cryptographic signature accompanying the packet (hex-encoded).
    data : dict | None
        Payload of the packet.

    Returns
    -------
    dict | None
        The original data dictionary if the signature is valid, otherwise None.

    Raises
    ------
    ConnectionError
        If the packet data is missing or not a dictionary.
    """
    # Ensure we received something that looks like a packet
    if data is None or not isinstance(data, dict):
        raise ConnectionError("Data packet is missing or malformed")

    # Fetch the trusted signature for this device
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not expected_signature:
        # Unknown device – treat as untrusted
        return None

    # Compute the signature of the received data
    computed_signature = _compute_signature(data)

    # Use constant-time comparison to avoid timing attacks
    if hmac.compare_digest(computed_signature, expected_signature) and \
       hmac.compare_digest(signature.lower(), expected_signature.lower()):
        # Signature matches – trust the data
        return data

    # Invalid signature; do not expose any details to the caller
    return None