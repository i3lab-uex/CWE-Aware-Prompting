import json
import hashlib
from typing import Dict, Any

# Global mapping of device IDs to their trusted cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; in a real system these would be securely stored.
    "device_001": "5d41402abc4b2a76b9719d911017c592",
    "device_002": "7d793037a0760186574b0282f2f435e7",
    # Add more device ID → signature mappings as needed.
}

def _compute_signature(data: Dict[str, Any]) -> str:
    """
    Compute a deterministic SHA-256 signature for the given data dictionary.
    The dictionary is first serialized to JSON with sorted keys to ensure
    consistent ordering across invocations.
    """
    json_bytes = json.dumps(data, sort_keys=True).encode("utf-8")
    return hashlib.sha256(json_bytes).hexdigest()

def manage_data_packet(
    io_device_id: str,
    crypto_signature: str,
    packet_data: Dict[str, Any]
) -> Dict[str, Any] | None:
    """
    Validate and process an incoming data packet from an IoT device.

    Parameters
    ----------
    io_device_id : str
        The unique identifier of the IoT device that sent the packet.
    crypto_signature : str
        The cryptographic signature attached to the packet (hex digest).
    packet_data : dict
        The actual data or payload to be processed.

    Returns
    -------
    dict | None
        The packet data if the signature is verified successfully;
        otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the packet data is missing or cannot be processed.
    """
    # Basic sanity checks
    if not isinstance(io_device_id, str) or not io_device_id:
        raise ConnectionError("Invalid device ID received.")
    if packet_data is None or not isinstance(packet_data, dict):
        raise ConnectionError("Failed to receive valid packet data.")

    # Retrieve the trusted signature for this device
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(io_device_id)
    if not expected_signature:
        # Unknown device – treat as a security risk
        return None

    # Compute the signature of the received data
    computed_signature = _compute_signature(packet_data)

    # Compare signatures securely to mitigate timing attacks
    if not hashlib.compare_digest(computed_signature, crypto_signature):
        # Signature mismatch – data is untrusted
        return None

    # If signatures match, return the original packet data
    return packet_data