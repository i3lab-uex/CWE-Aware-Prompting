import hmac
import hashlib
from typing import Dict, Optional

# Global dictionary mapping device IDs to their expected HMAC signatures.
# In a real deployment this would be populated from secure configuration
# or a secrets store. For illustration, we provide an example entry.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # device_id : hex-encoded HMAC signature
    "device_001": "a3f5c2e7b1d4c8e6f9a0b12345678901",
    # Add more device signatures as needed
}


def _compute_hmac(message: bytes, key: str) -> str:
    """
    Compute the HMAC-SHA256 of a message using a shared key.
    Returns a hex-encoded string.
    """
    mac = hmac.new(key.encode("utf-8"), message, hashlib.sha256)
    return mac.hexdigest()


def process_iot_packet(
    device_id: str,
    crypt_sig: str,
    pkt_data: Dict
) -> Optional[Dict]:
    """
    Validate the cryptographic signature of an IoT packet and process it.

    Parameters
    ----------
    device_id : str
        Unique identifier of the sending IoT device.
    crypt_sig : str
        Hex-encoded cryptographic signature provided with the packet.
    pkt_data : dict
        The payload of the IoT data packet.

    Returns
    -------
    dict | None
        Processed data if signature verification succeeds; otherwise None.

    Raises
    ------
    ConnectionError
        If the packet cannot be received or is malformed.
    """
    # 1. Basic sanity checks
    if not isinstance(pkt_data, dict):
        raise ConnectionError("Packet data is missing or corrupted.")

    # 2. Ensure the device is known
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if expected_sig is None:
        # Unknown device; treat as potential spoofing attempt
        return None

    # 3. Reconstruct the message that should have been signed.
    #    For this example we simply serialize pkt_data to a canonical JSON string.
    try:
        import json
        message = json.dumps(pkt_data, sort_keys=True).encode("utf-8")
    except Exception as exc:
        raise ConnectionError(f"Failed to serialize packet data: {exc}") from exc

    # 4. Compute the HMAC using a shared secret.
    #    In practice, each device would have its own secret key.
    #    Here we simulate with a deterministic placeholder key derived from the device_id.
    shared_key = f"secret_for_{device_id}"
    computed_sig = _compute_hmac(message, shared_key)

    # 5. Compare signatures using constant-time comparison to mitigate timing attacks.
    if not hmac.compare_digest(computed_sig, crypt_sig):
        # Signature mismatch – reject packet
        return None

    # 6. At this point, authenticity is verified.
    #    The packet can be processed safely. For demonstration, we simply return the data.
    #    Real processing logic (e.g., storing to DB, triggering actions) would be inserted here.
    return pkt_data