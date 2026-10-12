import hmac
import hashlib
from typing import Dict, Optional

# Global mapping of device IDs to their secret keys (not real signatures).
TRUSTED_DEVICE_SIGNATURES: Dict[str, bytes] = {
    # Example entries; in production these would be securely stored.
    "device_001": b"supersecretkey1",
    "device_002": b"anothersecurekey2",
}

def _verify_signature(secret: bytes, data: Dict, signature_hex: str) -> bool:
    """
    Verify that the provided hexadecimal signature matches an HMAC-SHA256
    computed over the JSON representation of `data` using `secret`.
    """
    # Serialize data in a deterministic way
    import json
    serialized = json.dumps(data, sort_keys=True).encode("utf-8")

    # Compute HMAC
    mac = hmac.new(secret, serialized, hashlib.sha256).hexdigest()

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(mac, signature_hex.lower())

def process_iot_packet(
    device_id: str,
    crypt_sig: str,
    pkt_data: Dict
) -> Optional[Dict]:
    """
    Validate and process an IoT packet.

    Parameters
    ----------
    device_id : str
        Unique identifier of the sending IoT device.
    crypt_sig : str
        Hexadecimal HMAC-SHA256 signature accompanying the packet.
    pkt_data : dict
        Payload of the packet.

    Returns
    -------
    dict or None
        The processed data if verification succeeds; otherwise `None`.

    Raises
    ------
    ConnectionError
        If the packet cannot be received (e.g., missing data).
    """
    # Basic sanity check: pkt_data must be a dictionary
    if not isinstance(pkt_data, dict):
        raise ConnectionError("Invalid packet format received.")

    # Retrieve the secret key for this device
    secret = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if secret is None:
        # Unknown device – treat as untrusted
        return None

    # Verify the cryptographic signature
    if not _verify_signature(secret, pkt_data, crypt_sig):
        # Signature mismatch – reject the packet
        return None

    # At this point, data authenticity is confirmed.
    # Perform any domain‑specific processing here. For demonstration,
    # simply return the packet data unchanged.
    processed = pkt_data.copy()
    # Example: add a timestamp of processing
    import time
    processed["processed_at"] = int(time.time())

    return processed