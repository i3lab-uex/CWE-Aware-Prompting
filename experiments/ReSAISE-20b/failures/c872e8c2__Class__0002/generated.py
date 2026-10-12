import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their trusted cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (replace with real values in production)
    "device-001": "f2a1c3b4d5e6f7g8h9i0j1k2l3m4n5o6",
    "device-002": "a1b2c3d4e5f678901234567890abcdef",
    # Add more device IDs and signatures as needed.
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
        The packet_data dictionary if the signature is verified successfully;
        otherwise, None.

    Raises
    ------
    ConnectionError
        If there are any issues receiving a data packet from the device,
        such as missing fields or invalid data types.
    """
    # Basic sanity checks for the inputs
    if not isinstance(io_device_id, str) or not io_device_id:
        raise ConnectionError("Invalid or missing device ID.")

    if not isinstance(crypto_signature, str) or not crypto_signature:
        raise ConnectionError("Missing cryptographic signature.")

    if not isinstance(packet_data, dict):
        raise ConnectionError("Packet data must be a dictionary.")

    # Retrieve the trusted signature for this device
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(io_device_id)

    if expected_signature is None:
        # Unknown device – treat as a connection error
        raise ConnectionError(f"Unknown device ID: {io_device_id}")

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(crypto_signature, expected_signature):
        # Signature does not match – do not trust the data
        return None

    # At this point, the packet is authenticated.
    # Perform any additional processing here (e.g., validation of payload fields).
    return packet_data