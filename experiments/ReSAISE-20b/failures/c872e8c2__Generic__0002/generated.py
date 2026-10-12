import hmac
from typing import Dict, Any

# Example trusted signatures mapping (should be populated securely in real usage)
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # "device_id": "expected_signature",
}

def manage_data_packet(
    io_device_id: str,
    crypto_signature: str,
    packet_data: Dict[str, Any]
) -> Dict[str, Any] | None:
    """
    Validate and process an incoming data packet from an IoT device.

    Parameters
    ----------
    io_device_id : str
        Unique identifier of the IoT device that sent the packet.
    crypto_signature : str
        Cryptographic signature attached to the packet (hex-encoded).
    packet_data : dict
        Payload of the data packet.

    Returns
    -------
    dict | None
        The original `packet_data` if the signature is verified; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the device is unknown or a communication error occurs.
    """
    # Ensure we have a trusted signature for the device
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(io_device_id)
    if expected_sig is None:
        # The device is unknown or not configured
        raise ConnectionError(f"Unrecognized IoT device ID: {io_device_id}")

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(crypto_signature, expected_sig):
        # Signature mismatch – data is untrusted
        return None

    # Signature verified; return the payload
    return packet_data