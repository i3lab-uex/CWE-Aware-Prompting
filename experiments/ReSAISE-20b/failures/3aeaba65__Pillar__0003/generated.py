import hmac
from typing import Dict, Any, Optional

# Global mapping of device IDs to their expected cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; in a real system these would be securely stored.
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef1234",
    # ... add more device signatures as needed
}

def verify_iot_signature(
    iot_id: str,
    crypto_signature: str,
    packet_info: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Authenticate and process data packets from IoT devices.

    Parameters
    ----------
    iot_id : str
        Unique identifier for the IoT device sending the data.
    crypto_signature : str
        Cryptographic signature attached to the data packet.
    packet_info : dict
        The actual content of the packet to be processed.

    Returns
    -------
    dict | None
        The packet data if the signature is valid; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If there is an issue receiving data from the IoT device,
        such as an unknown device ID or missing signature.
    """
    # Ensure the device is known; otherwise we cannot trust any data from it.
    try:
        expected_signature = TRUSTED_DEVICE_SIGNATURES[iot_id]
    except KeyError as exc:
        # Unknown device – treat this as a connection issue.
        raise ConnectionError(f"Unknown IoT device ID: {iot_id}") from exc

    # Compare signatures using a constant‑time comparison to mitigate timing attacks.
    if not hmac.compare_digest(expected_signature, crypto_signature):
        # Invalid signature: do not expose the packet data.
        return None

    # Signature is valid; safely return the packet information.
    return packet_info