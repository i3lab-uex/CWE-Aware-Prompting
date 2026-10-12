import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their expected cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    "device-001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "device-002": "6cb75f9b1a3c2e8d0a7d5f4b6c1d9e8f",
    # Add more device signatures as needed.
}


def verify_iot_signature(
    iot_id: str, crypto_signature: str, packet_info: Dict
) -> Optional[Dict]:
    """
    Authenticate and process a data packet from an IoT device.

    Parameters
    ----------
    iot_id : str
        Unique identifier for the IoT device.
    crypto_signature : str
        Cryptographic signature attached to the packet.
    packet_info : dict
        The actual content of the data packet.

    Returns
    -------
    dict or None
        The packet content if signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If there was an issue receiving data from the device.
    """
    # Simulate a connectivity check: if packet_info contains an 'error' key, raise.
    if packet_info.get("error") == "connection_lost":
        raise ConnectionError(f"Unable to receive data from device {iot_id}")

    # Retrieve the expected signature for this device.
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(iot_id)
    if not expected_sig:
        # Unknown device – treat as invalid signature.
        return None

    # Use constant‑time comparison to mitigate timing attacks.
    if not hmac.compare_digest(crypto_signature, expected_sig):
        return None

    # Signature is valid – return the packet data.
    return packet_info