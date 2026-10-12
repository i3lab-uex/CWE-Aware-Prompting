import hmac
from typing import Dict, Optional

# Global dictionary mapping device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; replace with real device IDs and signatures.
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef1234",
}

def process_data_packet(dev_id: str, sign: str, payload: Dict) -> Optional[Dict]:
    """
    Validate and process an incoming data packet from an IoT device.

    Parameters
    ----------
    dev_id : str
        Unique identifier of the device that sent the packet.
    sign : str
        Cryptographic signature attached to the packet.
    payload : dict
        The actual data or payload to be processed.

    Returns
    -------
    dict | None
        The payload dictionary if the signature is verified successfully,
        otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the device is unknown or there is an issue receiving a packet.
    """
    # Ensure we have a trusted signature for the device
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(dev_id)
    if not expected_sig:
        # Device unknown or connection problem
        raise ConnectionError(f"Untrusted or missing device: {dev_id}")

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(sign, expected_sig):
        # Signature mismatch – data is untrusted
        return None

    # Signature verified; return the payload
    return payload