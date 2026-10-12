import hashlib
from typing import Dict, Optional

# Global mapping of device IDs to their trusted cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (replace with real values in production)
    "device-001": "a3f5c8d2e1b9...",
    "device-002": "4b7e9c3a2f6d...",
}

def _compute_signature(data: Dict) -> str:
    """
    Compute a deterministic cryptographic signature for the given data.
    Uses SHA-256 over the JSON string representation of the dictionary
    with sorted keys to ensure consistent ordering.
    """
    import json

    # Convert dict to JSON string with sorted keys for determinism
    data_str = json.dumps(data, sort_keys=True, separators=(",", ":"))
    # Compute SHA-256 hash
    return hashlib.sha256(data_str.encode("utf-8")).hexdigest()

def manage_data_packet(
    io_device_id: str,
    crypto_signature: str,
    packet_data: Dict
) -> Optional[Dict]:
    """
    Validate and process an incoming data packet from an IoT device.

    Parameters
    ----------
    io_device_id : str
        Unique identifier of the IoT device that sent the packet.
    crypto_signature : str
        Cryptographic signature attached to the packet.
    packet_data : dict
        The actual data or payload to be processed.

    Returns
    -------
    dict | None
        The packet data if the signature is verified successfully;
        otherwise, None.

    Raises
    ------
    ConnectionError
        If there are any issues receiving a data packet from a device,
        e.g., the device ID is unknown.
    """
    # Check that we have a trusted signature for this device
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(io_device_id)
    if expected_signature is None:
        # Device not registered or cannot be verified
        raise ConnectionError(f"Unknown device ID: {io_device_id}")

    # Verify the provided signature against the expected one
    if crypto_signature != expected_signature:
        return None

    # Optionally, double-check that the packet data matches its signature
    # (useful if signatures are computed on-the-fly rather than precomputed)
    try:
        computed_sig = _compute_signature(packet_data)
    except Exception as exc:
        # Any error during signature computation is treated as a communication issue
        raise ConnectionError(f"Failed to compute signature: {exc}") from exc

    if computed_sig != crypto_signature:
        # Signature mismatch; data might be tampered
        return None

    # At this point the packet is verified and can be safely returned
    return packet_data