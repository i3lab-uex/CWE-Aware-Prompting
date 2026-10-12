import hmac
import hashlib
from typing import Dict, Optional

# Global mapping of device IDs to their shared secret keys (used for HMAC signatures)
TRUSTED_DEVICE_SIGNATURES: Dict[str, bytes] = {
    # Example entries – replace with real device secrets
    "device_001": b"super_secret_key_for_device_001",
    "device_002": b"another_super_secret_key",
}

def process_packet_data(
    id_device: str,
    packet_signature: str,
    packet_data: Optional[Dict],
) -> Optional[Dict]:
    """
    Verify the cryptographic signature of a packet from an IoT device and
    return its data if valid.

    Parameters
    ----------
    id_device : str
        Unique identifier for the IoT device.
    packet_signature : str
        Hex-encoded HMAC-SHA256 signature attached to the packet.
    packet_data : dict | None
        The actual content of the packet.

    Returns
    -------
    dict | None
        The packet data if signature verification succeeds, otherwise None.

    Raises
    ------
    ConnectionError
        If packet data is missing or cannot be processed.
    """
    # Simulate a potential communication error
    if packet_data is None:
        raise ConnectionError("Failed to receive data from device")

    # Ensure the device is known
    secret_key = TRUSTED_DEVICE_SIGNATURES.get(id_device)
    if secret_key is None:
        # Unknown device – reject silently to avoid leaking info
        return None

    # Recreate the expected HMAC signature from the packet data
    try:
        # Serialize the data deterministically (e.g., JSON with sorted keys)
        import json
        packet_json = json.dumps(packet_data, separators=(",", ":"), sort_keys=True).encode("utf-8")
    except Exception as exc:
        raise ConnectionError(f"Invalid packet data format: {exc}") from exc

    expected_hmac = hmac.new(secret_key, packet_json, hashlib.sha256).hexdigest()

    # Use constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(expected_hmac, packet_signature.lower()):
        # Signature mismatch – reject the packet
        return None

    # All checks passed; return the verified data
    return packet_data