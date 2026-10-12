import hmac
import hashlib

# Example trusted device signatures (device_id -> signature)
TRUSTED_DEVICE_SIGNATURES = {
    "device_001": "f2ca1bb6c7e907d06dafe4687e579fce",
    "device_002": "3b5a1d4c2e7f9c1a8b0f6e3d5c4b2a1d",
    # Add more device signatures here
}

def process_packet_data(id_device: str, packet_signature: str, packet_data: dict) -> dict | None:
    """
    Authenticate and process data packets from IoT devices.

    Parameters
    ----------
    id_device : str
        Unique identifier of the device that sent the packet.
    packet_signature : str
        Cryptographic signature attached to the data packet.
    packet_data : dict
        Payload of the packet.

    Returns
    -------
    dict | None
        The packet data if the signature is valid, otherwise None.

    Raises
    ------
    ConnectionError
        If the packet data could not be received or is malformed.
    """
    # Basic sanity checks
    if packet_data is None:
        raise ConnectionError("No data received from device")

    if not isinstance(packet_data, dict):
        raise ConnectionError("Malformed packet data: expected a dictionary")

    # Retrieve the trusted signature for this device
    trusted_signature = TRUSTED_DEVICE_SIGNATURES.get(id_device)
    if not trusted_signature:
        # Device unknown – treat as unauthenticated
        return None

    # Verify the signature using constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(packet_signature, trusted_signature):
        return None

    # At this point the packet is authenticated; return its contents
    return packet_data