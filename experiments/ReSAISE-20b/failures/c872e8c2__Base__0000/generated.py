import json
import hmac
import hashlib
from typing import Dict, Optional

# Global dictionary mapping device IDs to their shared secret keys.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; in production these should be securely stored.
    "device-001": "s3cr3tK3yForDevice001",
    "device-002": "an0th3rS3cr3tK3y",
    # Add more device secrets here.
}


def _compute_hmac(secret_key: str, data: dict) -> str:
    """
    Compute the HMAC-SHA256 of a JSON-serialised payload using the provided secret key.
    The JSON is serialised with sorted keys to ensure deterministic ordering.
    """
    # Convert the payload to a canonical JSON string
    json_bytes = json.dumps(data, separators=(",", ":"), sort_keys=True).encode("utf-8")
    # Compute HMAC
    hmac_obj = hmac.new(secret_key.encode("utf-8"), json_bytes, hashlib.sha256)
    return hmac_obj.hexdigest()


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
        Cryptographic signature attached to the packet (hex string).
    packet_data : dict
        The actual data or payload to be processed.

    Returns
    -------
    dict | None
        The packet data if the signature is verified; otherwise, None.

    Raises
    ------
    ConnectionError
        If the packet could not be received or is malformed.
    """
    # Basic sanity checks
    if not isinstance(io_device_id, str) or not io_device_id:
        raise ConnectionError("Invalid device ID received.")
    if not isinstance(crypto_signature, str) or not crypto_signature:
        raise ConnectionError("Missing cryptographic signature.")
    if not isinstance(packet_data, dict):
        raise ConnectionError("Packet data must be a dictionary.")

    # Retrieve the trusted secret key for this device
    secret_key = TRUSTED_DEVICE_SIGNATURES.get(io_device_id)
    if not secret_key:
        # Unknown device – treat as a connection issue
        raise ConnectionError(f"Unknown or untrusted device ID: {io_device_id}")

    # Compute the expected signature
    try:
        expected_signature = _compute_hmac(secret_key, packet_data)
    except Exception as exc:
        # Any error during HMAC computation is treated as a connection issue
        raise ConnectionError("Failed to compute signature.") from exc

    # Constant-time comparison to prevent timing attacks
    if hmac.compare_digest(expected_signature, crypto_signature):
        return packet_data  # Signature verified
    else:
        # Invalid signature – do not trust the data
        return None