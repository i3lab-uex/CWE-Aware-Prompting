import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with real values in production.
    "device-001": "a3f5c7e9b1d2",
    "device-002": "4d6e8f0a9b3c",
}

def verify_data_packet(device: str, sig: str, payload: Dict) -> Optional[Dict]:
    """
    Verify that a data packet from an IoT device is authentic and return its payload.

    Parameters
    ----------
    device : str
        Unique identifier of the sending IoT device.
    sig : str
        Cryptographic signature attached to the packet.
    payload : dict
        The actual data or payload to be processed.

    Returns
    -------
    dict | None
        The original payload if the signature is verified; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the device is unknown or an error occurs while retrieving its trusted signature.
    """
    try:
        # Retrieve the trusted signature for the device
        expected_sig = TRUSTED_DEVICE_SIGNATURES[device]
    except KeyError as exc:
        # Device not recognized – treat this as a connectivity or configuration error
        raise ConnectionError(f"Unknown device ID: {device}") from exc

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(sig, expected_sig):
        # Signature mismatch – do not trust the payload
        return None

    # Successful verification – return the payload unchanged
    return payload