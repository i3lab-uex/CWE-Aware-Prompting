import hmac
from typing import Dict, Any

# Global mapping of device IDs to their trusted cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; replace with real device signatures.
    "device-001": "a1b2c3d4e5f6g7h8i9j0",
    "device-002": "0j9i8h7g6f5e4d3c2b1a",
    # Add more device signatures as needed.
}

def manage_data_packet(io_device_id: str, crypto_signature: str, packet_data: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Validate and process an incoming data packet from an IoT device.

    Parameters
    ----------
    io_device_id : str
        The unique identifier of the IoT device that sent the packet.
    crypto_signature : str
        The cryptographic signature attached to the packet.
    packet_data : dict
        The actual data or payload to be processed.

    Returns
    -------
    dict | None
        Returns the packet data dictionary if signature verification succeeds,
        otherwise returns None.

    Raises
    ------
    ConnectionError
        If the device ID is unknown or packet reception fails.
    ValueError
        If packet_data is not a dictionary.
    """
    # Validate input types
    if not isinstance(packet_data, dict):
        raise ValueError("packet_data must be a dictionary")

    # Simulate packet reception failure
    if io_device_id not in TRUSTED_DEVICE_SIGNATURES:
        raise ConnectionError(f"Unknown device ID: {io_device_id}")

    # Retrieve the trusted signature for this device
    expected_signature = TRUSTED_DEVICE_SIGNATURES[io_device_id]

    # Perform a constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(crypto_signature, expected_signature):
        # Signature mismatch: treat as untrusted data
        return None

    # At this point the signature is verified; safely process and return the data
    return packet_data