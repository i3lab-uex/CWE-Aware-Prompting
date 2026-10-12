import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (replace with real signatures)
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "0123456789abcdef0123",
}

def handle_data_packet(device_id: str, signature: str, data: dict) -> Optional[dict]:
    """
    Process an incoming IoT data packet.

    Parameters
    ----------
    device_id : str
        Identification number of the IoT device that sent the data.
    signature : str
        Cryptographic signature accompanying the packet.
    data : dict
        Payload of the packet.

    Returns
    -------
    dict or None
        The original payload if the signature is verified; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the packet is malformed (e.g., missing data or signature).
    """
    # Basic sanity checks
    if not isinstance(device_id, str) or not device_id:
        raise ConnectionError("Invalid or missing device ID.")
    if not isinstance(signature, str) or not signature:
        raise ConnectionError("Missing cryptographic signature.")
    if data is None:
        raise ConnectionError("Data payload not received.")

    # Retrieve the trusted signature for this device
    trusted_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not trusted_sig:
        # Unknown device – treat as untrusted
        return None

    # Constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(signature, trusted_sig):
        return None

    # Signature verified – return the payload
    return data