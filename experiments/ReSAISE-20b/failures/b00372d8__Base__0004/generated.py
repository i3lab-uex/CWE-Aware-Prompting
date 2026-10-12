import hmac
import hashlib
from typing import Dict, Optional

# Global dictionary mapping device IDs to their HMAC secret keys (hex encoded)
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (device_id: secret_key_hex)
    "device_001": "a1b2c3d4e5f60718293a4b5c6d7e8f90",
    "device_002": "0fedcba98765432100123456789abcdef",
}

def _compute_hmac(secret_hex: str, data_bytes: bytes) -> str:
    """
    Compute the HMAC-SHA256 of the given data using the provided secret key.
    Returns the hex digest string.
    """
    secret = bytes.fromhex(secret_hex)
    return hmac.new(secret, data_bytes, hashlib.sha256).hexdigest()

def process_iot_packet(
    device_id: str,
    crypt_sig: str,
    pkt_data: Optional[Dict]
) -> Optional[Dict]:
    """
    Validate the cryptographic signature of an IoT packet and process it.

    Parameters
    ----------
    device_id : str
        Unique identifier for the IoT device.
    crypt_sig : str
        Hex-encoded signature sent with the packet.
    pkt_data : dict or None
        The content of the data packet.

    Returns
    -------
    dict | None
        Processed data if validation succeeds, otherwise None.

    Raises
    ------
    ConnectionError
        If the packet could not be received (pkt_data is None).
    """
    if pkt_data is None:
        # Simulate a failure to receive the packet
        raise ConnectionError(f"Packet from device {device_id} could not be received.")

    # Ensure the device is trusted
    secret_hex = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not secret_hex:
        # Device not recognized; treat as invalid
        return None

    # Serialize the packet data deterministically (JSON string)
    import json
    pkt_json = json.dumps(pkt_data, sort_keys=True).encode("utf-8")

    # Compute the expected signature
    expected_sig = _compute_hmac(secret_hex, pkt_json)

    # Constant-time comparison to prevent timing attacks
    if not hmac.compare_digest(expected_sig, crypt_sig.lower()):
        # Signature mismatch
        return None

    # At this point the signature is valid; process the data.
    # For demonstration, we simply return a shallow copy of pkt_data.
    processed = dict(pkt_data)
    # Example processing: add a timestamp or validation flag
    processed["validated"] = True

    return processed