import hmac
from typing import Dict, Optional

# Global dictionary mapping device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; in production these would be securely stored.
    "device-001": "a1b2c3d4e5f6g7h8i9j0",
    "device-002": "1234567890abcdef0123",
}


def verify_data_packet(device: str, sig: str, payload: Dict) -> Optional[Dict]:
    """
    Validate and process an incoming data packet from an IoT device.

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
        Returns the payload dictionary if signature verification succeeds,
        otherwise returns ``None``.

    Raises
    ------
    ConnectionError
        If there is an issue receiving the data packet from the device.
    TypeError
        If arguments are of incorrect type.

    Notes
    -----
    This function uses constant‑time comparison (``hmac.compare_digest``) to
    mitigate timing attacks and follows the CWE‑693 best practice of using a
    reliable protection mechanism for signature verification.
    """
    # Basic type validation to avoid malformed inputs.
    if not isinstance(device, str):
        raise TypeError("device must be a string")
    if not isinstance(sig, str):
        raise TypeError("sig must be a string")
    if not isinstance(payload, dict):
        raise TypeError("payload must be a dictionary")

    # Retrieve the trusted signature for this device.
    try:
        expected_sig = TRUSTED_DEVICE_SIGNATURES[device]
    except KeyError as exc:
        # The device is unknown; treat this as a reception issue.
        raise ConnectionError(f"Untrusted or unknown device: {device}") from exc

    # Perform constant‑time comparison of signatures.
    if not hmac.compare_digest(sig, expected_sig):
        # Signature mismatch – do not process the payload.
        return None

    # At this point, signature is verified; safely return the payload.
    return payload