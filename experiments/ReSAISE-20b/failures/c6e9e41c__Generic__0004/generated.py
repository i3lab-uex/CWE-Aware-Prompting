import hmac
from typing import Dict, Optional

# Global dictionary mapping device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; replace with actual values.
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef1234",
}

def verify_data_packet(
    device: str,
    sig: str,
    payload: Dict
) -> Optional[Dict]:
    """
    Validate an incoming data packet from an IoT device.

    Parameters
    ----------
    device : str
        Unique identifier of the sending IoT device.
    sig : str
        Cryptographic signature attached to the packet (hex string).
    payload : dict
        The actual data payload.

    Returns
    -------
    dict or None
        The original payload if the signature is verified; otherwise `None`.

    Raises
    ------
    ConnectionError
        If the packet could not be received or the device is unknown.
    """
    # Check that we actually have a payload to work with
    if not isinstance(payload, dict):
        raise ConnectionError("Invalid or missing payload received.")

    # Retrieve the trusted signature for this device
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(device)
    if expected_sig is None:
        raise ConnectionError(f"Unknown device: {device}")

    # Perform a constant‑time comparison to avoid timing attacks
    if hmac.compare_digest(sig, expected_sig):
        return payload

    # Signature mismatch; do not trust the data
    return None