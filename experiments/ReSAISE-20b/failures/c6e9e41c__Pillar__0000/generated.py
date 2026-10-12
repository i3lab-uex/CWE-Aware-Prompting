import secrets
from typing import Dict, Optional

# Global dictionary mapping device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries – in production these would be securely stored
    "device-001": "a1b2c3d4e5f6g7h8i9j0",
    "device-002": "1234567890abcdef1234",
}

def verify_data_packet(device: str, sig: str, payload: Optional[Dict]) -> Optional[Dict]:
    """
    Validate an incoming data packet from an IoT device.

    Parameters
    ----------
    device : str
        The unique identifier of the IoT device that sent the packet.
    sig : str
        The cryptographic signature attached to the packet.
    payload : dict or None
        The actual data or payload to be processed.

    Returns
    -------
    dict | None
        The original payload dictionary if the signature is verified.
        Returns None if verification fails.

    Raises
    ------
    ConnectionError
        If the packet is missing critical information or cannot be received.
    """
    # Ensure we actually received a payload
    if payload is None:
        raise ConnectionError(f"No payload received from device {device}")

    # Ensure the device is known
    trusted_sig = TRUSTED_DEVICE_SIGNATURES.get(device)
    if not trusted_sig:
        raise ConnectionError(f"Unknown device ID: {device}")

    # Constant‑time comparison to mitigate timing attacks (CWE‑693)
    if not secrets.compare_digest(sig, trusted_sig):
        # Signature mismatch – do not trust the payload
        return None

    # At this point, signature is verified; return a copy to avoid accidental mutation
    return dict(payload)