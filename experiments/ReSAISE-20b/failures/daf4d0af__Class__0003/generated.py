import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (replace with real values)
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef1234",
}

def handle_data_packet(
    device_id: str,
    signature: str,
    data: Dict
) -> Optional[Dict]:
    """
    Process a data packet from an IoT device after verifying its cryptographic signature.

    Parameters
    ----------
    device_id : str
        Identifier of the IoT device that sent the packet.
    signature : str
        Cryptographic signature accompanying the packet.
    data : dict
        Payload of the packet.

    Returns
    -------
    dict | None
        The payload if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the packet is malformed (e.g., missing fields or wrong types).
    """
    # Basic sanity checks to guard against malformed packets.
    if not isinstance(device_id, str):
        raise ConnectionError("Device ID must be a string.")
    if not isinstance(signature, str):
        raise ConnectionError("Signature must be a string.")
    if not isinstance(data, dict):
        raise ConnectionError("Data payload must be a dictionary.")

    # Retrieve the trusted signature for this device, if any.
    trusted_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not trusted_sig:
        # Unknown device – treat as untrusted.
        return None

    # Use constant‑time comparison to avoid timing attacks.
    if not hmac.compare_digest(signature, trusted_sig):
        # Signature mismatch – data is untrusted.
        return None

    # All checks passed; the packet is trusted.
    return data