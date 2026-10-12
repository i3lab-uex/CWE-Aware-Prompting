import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their trusted signatures.
# In a real deployment this would be loaded from secure storage
# and never hard‑coded.  For demonstration purposes it is kept simple.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # device_id: signature
    "device_001": "5f2c8e3a1d4b9f7c6e0d12ab34cd5678",
    "device_002": "a1b2c3d4e5f67890abcdef1234567890",
    # Add additional trusted devices here
}


def verify_data_packet(device: str, sig: str, payload: Dict) -> Optional[Dict]:
    """
    Validate the cryptographic signature of a data packet from an IoT device.

    Parameters
    ----------
    device : str
        Unique identifier of the IoT device that sent the packet.
    sig : str
        Cryptographic signature attached to the packet.
    payload : dict
        The actual data or payload to be processed.

    Returns
    -------
    dict | None
        Returns the payload if the signature is verified successfully;
        otherwise returns None.

    Raises
    ------
    ConnectionError
        If the device is unknown or there was an issue retrieving its trusted signature.
    """
    # Ensure that the device ID is known
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(device)
    if expected_sig is None:
        # Device not recognized – treat as a communication error
        raise ConnectionError(f"Unrecognized device ID: {device}")

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(expected_sig, sig):
        # Signature mismatch – do not trust the payload
        return None

    # All checks passed; return the trusted data
    return payload