import json
import hashlib
from typing import Dict, Any

# Global mapping of device IDs to their expected cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; in a real system these would be securely stored.
    "device_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "device_002": "6c0b8e3d1f4a7b2c9e5d4f6a8b0c3d1e",
    # Add more trusted devices here.
}

def _compute_packet_hash(pkt_data: Dict[str, Any]) -> str:
    """
    Compute a deterministic SHA256 hash of the packet data.
    The packet is first serialized to JSON with sorted keys to ensure
    consistent ordering across different systems.
    """
    json_bytes = json.dumps(pkt_data, sort_keys=True).encode("utf-8")
    return hashlib.sha256(json_bytes).hexdigest()

def process_iot_packet(device_id: str, crypt_sig: str, pkt_data: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Validate the cryptographic signature of an IoT packet and process it.

    Parameters
    ----------
    device_id : str
        Unique identifier of the IoT device.
    crypt_sig : str
        Cryptographic signature sent with the packet (hex string).
    pkt_data : dict
        The content of the data packet to be processed.

    Returns
    -------
    dict | None
        The processed packet if validation succeeds; otherwise None.

    Raises
    ------
    ConnectionError
        If the packet cannot be received (e.g., missing data or unknown device).
    """
    # Basic sanity checks
    if pkt_data is None:
        raise ConnectionError(f"Packet from device {device_id} could not be received.")

    if device_id not in TRUSTED_DEVICE_SIGNATURES:
        raise ConnectionError(f"Unknown device ID: {device_id}")

    # Retrieve the expected signature for this device
    expected_sig = TRUSTED_DEVICE_SIGNATURES[device_id]

    # Compute the hash of the received packet
    computed_sig = _compute_packet_hash(pkt_data)

    # Compare signatures securely (constant‑time comparison to avoid timing attacks)
    if not hashlib.compare_digest(computed_sig, crypt_sig):
        # Signature mismatch; reject packet
        return None

    # At this point the signature is valid. Perform any processing needed.
    # For demonstration, we simply return a copy of the packet data with an
    # added "validated" flag.
    processed = pkt_data.copy()
    processed["validated"] = True
    return processed