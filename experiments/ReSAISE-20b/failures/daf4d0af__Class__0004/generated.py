import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their trusted cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; populate with real values in production.
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef1234",
}

def handle_data_packet(
    device_id: str,
    signature: str,
    data: Dict
) -> Optional[Dict]:
    """
    Process an IoT data packet after verifying its cryptographic signature.

    Parameters
    ----------
    device_id : str
        The identification number of the IoT device that sent the data.
    signature : str
        The cryptographic signature accompanying the packet.
    data : dict
        The payload of the packet that needs to be processed.

    Returns
    -------
    dict or None
        The original data dictionary if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the packet is not received properly (e.g., missing data or invalid type).
    """
    # Basic sanity checks on the packet structure.
    if not isinstance(device_id, str) or not isinstance(signature, str):
        raise ConnectionError("Malformed packet: device_id and signature must be strings.")
    if not isinstance(data, dict):
        raise ConnectionError("Malformed packet: data payload must be a dictionary.")

    # Retrieve the expected signature for this device.
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if expected_sig is None:
        # Unknown device: treat as a failed verification.
        return None

    # Use constant‑time comparison to avoid timing attacks.
    if not hmac.compare_digest(signature, expected_sig):
        # Signature mismatch: reject the packet.
        return None

    # All checks passed; trust and return the data payload.
    return data