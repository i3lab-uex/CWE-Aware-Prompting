import hmac
from typing import Dict, Optional

# Global dictionary mapping device IDs to their trusted cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with real signatures in production.
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "0123456789abcdef1234",
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
        Returns the packet data if signature verification succeeds,
        otherwise returns None.

    Raises
    ------
    ConnectionError
        If the packet data cannot be received or is malformed.
    """
    # Simulate a potential issue in receiving the packet
    if packet_data is None:
        raise ConnectionError("Failed to receive data packet from device.")

    # Ensure the packet data is a dictionary
    if not isinstance(packet_data, dict):
        raise ConnectionError("Packet payload must be a dictionary.")

    # Retrieve the trusted signature for this device
    trusted_sig = TRUSTED_DEVICE_SIGNATURES.get(io_device_id)
    if not trusted_sig:
        # Unknown device – treat as untrusted
        return None

    # Use constant‑time comparison to prevent timing attacks (CWE‑693)
    if hmac.compare_digest(crypto_signature, trusted_sig):
        # Signature verified – return the data
        return packet_data

    # Signature mismatch – do not trust the payload
    return None