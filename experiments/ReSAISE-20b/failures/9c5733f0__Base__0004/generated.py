import json
import hmac
import hashlib
from typing import Dict, Optional

# Global dictionary mapping device IDs to their shared secret keys.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (hex‑encoded secret keys)
    "device_001": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6",
    "device_002": "f0e1d2c3b4a5f6e7d8c9b0a1b2c3d4e5",
    # Add more devices as needed
}

def _serialize_packet(packet: Dict) -> bytes:
    """
    Serialize the packet data deterministically to a JSON byte string.
    The serialization order must be consistent for signature verification.
    """
    # Sort keys to ensure deterministic ordering
    return json.dumps(packet, separators=(",", ":"), sort_keys=True).encode("utf-8")

def _verify_signature(secret: str, payload: bytes, signature_hex: str) -> bool:
    """
    Verify that the provided hex signature matches the HMAC-SHA256 of payload
    using the given secret key.
    """
    # Convert hex-encoded secret to bytes
    try:
        secret_bytes = bytes.fromhex(secret)
    except ValueError:
        return False

    # Compute HMAC
    computed_hmac = hmac.new(secret_bytes, payload, hashlib.sha256).hexdigest()

    # Use constant‑time comparison
    return hmac.compare_digest(computed_hmac, signature_hex)

def process_packet_data(
    id_device: str,
    packet_signature: str,
    packet_data: Dict
) -> Optional[Dict]:
    """
    Authenticate an IoT data packet and return the packet content if the
    signature is valid.

    Parameters:
        id_device (str): Unique identifier of the sending device.
        packet_signature (str): Hex‑encoded cryptographic signature
                                attached to the packet.
        packet_data (dict): The actual content of the packet.

    Returns:
        dict: The packet data if authentication succeeds.
        None: If the signature is invalid.

    Raises:
        ConnectionError: If there was an error receiving or processing
                         the packet (e.g., malformed data).
    """
    try:
        # Ensure device is known
        if id_device not in TRUSTED_DEVICE_SIGNATURES:
            return None

        # Serialize packet deterministically
        payload = _serialize_packet(packet_data)

        # Retrieve the shared secret key for this device
        secret_key = TRUSTED_DEVICE_SIGNATURES[id_device]

        # Verify the signature
        if not _verify_signature(secret_key, payload, packet_signature):
            return None

        # Signature is valid; return the original data
        return packet_data

    except Exception as exc:
        # Any unexpected error during processing is treated as a connection issue
        raise ConnectionError("Failed to receive or process packet data") from exc