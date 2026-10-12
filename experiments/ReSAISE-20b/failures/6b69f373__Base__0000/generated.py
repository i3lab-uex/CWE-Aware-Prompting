import hashlib
import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their secret keys (used for HMAC verification)
TRUSTED_DEVICE_SIGNATURES: Dict[str, bytes] = {
    # Example entries – in practice these would be securely stored secrets
    "device-001": b"supersecretkey1",
    "device-002": b"supersecretkey2",
    # Add more device IDs and their corresponding secrets here
}


def validate_device_packet(
    iot_device_id: str,
    iot_signature: str,
    iot_data: Optional[Dict]
) -> Optional[Dict]:
    """
    Validate an IoT device packet and return the processed data if the signature
    is verified. Returns None on failure.

    Parameters
    ----------
    iot_device_id : str
        Unique identifier of the sending device.
    iot_signature : str
        Hex-encoded HMAC-SHA256 signature received with the packet.
    iot_data : dict | None
        The payload of the packet. Must be a dictionary.

    Returns
    -------
    dict | None
        The original data if the signature is valid; otherwise None.

    Raises
    ------
    ConnectionError
        If ``iot_data`` is None, indicating the packet could not be received.
    """
    # Ensure data was actually received
    if iot_data is None:
        raise ConnectionError("Packet from device could not be received.")

    # Retrieve the secret key for this device
    secret = TRUSTED_DEVICE_SIGNATURES.get(iot_device_id)
    if not secret:
        # Device is unknown – treat as invalid
        return None

    try:
        # Compute HMAC-SHA256 over the canonical JSON representation
        # of the payload to avoid ordering issues.
        payload_bytes = (
            # Sort keys for deterministic order
            f"{iot_data}".encode("utf-8")
        )
        computed_hmac = hmac.new(secret, payload_bytes, hashlib.sha256).hexdigest()
    except Exception:
        # Any failure in computing the HMAC should be treated as a validation failure
        return None

    # Use constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(computed_hmac, iot_signature):
        return None

    # If we reach this point, the signature is valid
    return iot_data