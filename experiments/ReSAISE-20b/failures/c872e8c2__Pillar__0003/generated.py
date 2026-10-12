import hmac
from typing import Dict, Optional

# Global mapping of trusted device IDs to their expected cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with real signatures in production.
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef1234",
}

def manage_data_packet(
    io_device_id: str,
    crypto_signature: str,
    packet_data: Dict
) -> Optional[Dict]:
    """
    Validate and process an incoming data packet from an IoT device.

    Parameters
    ----------
    io_device_id : str
        Unique identifier of the IoT device that sent the packet.
    crypto_signature : str
        Cryptographic signature attached to the packet.
    packet_data : dict
        The actual data or payload to be processed.

    Returns
    -------
    dict | None
        The packet data if the signature is verified; otherwise, None.

    Raises
    ------
    ConnectionError
        If the packet data is missing or not a dictionary.
    """
    # Ensure we received valid payload
    if packet_data is None or not isinstance(packet_data, dict):
        raise ConnectionError("Failed to receive valid data packet from device.")

    # Retrieve the expected signature for this device.
    try:
        expected_sig = TRUSTED_DEVICE_SIGNATURES[io_device_id]
    except KeyError as exc:
        # Device not registered – treat as a potential compromise.
        raise ConnectionError(f"Unrecognized device ID: {io_device_id}") from exc

    # Compare signatures in constant time to mitigate timing attacks.
    if not hmac.compare_digest(expected_sig, crypto_signature):
        # Signature mismatch – do not trust the data.
        return None

    # Signature verified – return the payload unchanged.
    return packet_data