import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (in a real system these would be securely stored)
    "device-001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "device-002": "6c569aabbf7775ef8fc570e228c16b98",
    # ... add more device signatures as needed
}


def validate_device_packet(
    iot_device_id: str,
    iot_signature: str,
    iot_data: Dict,
) -> Optional[Dict]:
    """
    Validate the cryptographic signature of an IoT device packet and return
    the processed data if validation succeeds.

    Parameters
    ----------
    iot_device_id : str
        Unique identifier of the IoT device sending the packet.
    iot_signature : str
        Cryptographic signature accompanying the data packet.
    iot_data : dict
        Payload of the data packet to be processed.

    Returns
    -------
    Optional[dict]
        The original `iot_data` if the signature is valid; otherwise None.

    Raises
    ------
    ConnectionError
        If the device ID is unknown or packet cannot be received.
    """
    # Ensure the device ID exists in our trusted list
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(iot_device_id)
    if expected_signature is None:
        # Unknown device: treat as a connection error
        raise ConnectionError(f"Unknown device ID '{iot_device_id}'")

    # Compare signatures using a constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(iot_signature, expected_signature):
        # Signature mismatch: do not process the data
        return None

    # At this point the signature is verified; we can safely process the data
    return iot_data