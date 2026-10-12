import hmac
import hashlib
from datetime import datetime, timezone
from typing import Dict, Optional

# Global dictionary mapping device IDs to their secret keys (hex‑encoded)
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with real keys
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef1234",
}

def _compute_hmac(secret_key: str, message: bytes) -> str:
    """
    Compute an HMAC-SHA256 over *message* using the provided secret key.
    The key is expected to be a hex string; it will be decoded before use.
    Returns the resulting HMAC as a lowercase hexadecimal string.
    """
    key_bytes = bytes.fromhex(secret_key)
    return hmac.new(key_bytes, message, hashlib.sha256).hexdigest()

def process_packet(
    device_id: str,
    packet_signature: str,
    data_packet: Optional[Dict],
) -> Optional[Dict]:
    """
    Validate and process a packet received from an IoT device.

    Parameters
    ----------
    device_id : str
        Unique identifier of the sending IoT device.
    packet_signature : str
        Hex‑encoded cryptographic signature sent with the packet.
    data_packet : dict | None
        The content of the data packet to be processed.

    Returns
    -------
    dict | None
        The processed packet if the signature is valid; otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the packet cannot be received (i.e., ``data_packet`` is ``None``).
    """
    # Simulate a failure to receive the packet
    if data_packet is None:
        raise ConnectionError(f"Failed to receive packet from device {device_id}")

    # Retrieve the expected secret key for this device
    secret_key = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not secret_key:
        # Unknown device – treat as invalid
        return None

    try:
        # Serialize the data packet to a canonical byte representation.
        # We use JSON with sorted keys to ensure deterministic ordering.
        import json
        message_bytes = json.dumps(data_packet, sort_keys=True).encode("utf-8")
    except (TypeError, ValueError) as exc:
        # If the packet cannot be serialized, treat it as invalid
        return None

    # Compute the expected HMAC signature
    expected_sig = _compute_hmac(secret_key, message_bytes)

    # Use a timing‑attack resistant comparison
    if not hmac.compare_digest(expected_sig, packet_signature.lower()):
        # Signature mismatch – reject the packet
        return None

    # If we reach here, the signature is valid.
    # Perform minimal processing – e.g., add a processed timestamp.
    processed_packet = dict(data_packet)  # shallow copy
    processed_packet["processed_at"] = datetime.now(timezone.utc).isoformat()

    return processed_packet