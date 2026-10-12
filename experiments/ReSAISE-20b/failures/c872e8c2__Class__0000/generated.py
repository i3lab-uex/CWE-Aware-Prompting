import hmac
import hashlib

# Global dictionary mapping device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES = {
    # Example entries – in a real system these would be securely stored.
    "device_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "device_002": "e99a18c428cb38d5f260853678922e03",
    # Add more device signatures as needed.
}

def manage_data_packet(io_device_id: str, crypto_signature: str, packet_data: dict) -> dict | None:
    """
    Validate the cryptographic signature of an incoming data packet from an IoT device
    and return the packet payload if the signature is verified.

    Parameters
    ----------
    io_device_id : str
        Unique identifier of the IoT device that sent the packet.
    crypto_signature : str
        Cryptographic signature attached to the packet (hex encoded).
    packet_data : dict
        The actual data or payload that was sent.

    Returns
    -------
    dict | None
        The packet_data dictionary if the signature is verified; otherwise None.

    Raises
    ------
    ConnectionError
        If the packet could not be received (e.g., missing data or device unknown).
    """
    # Ensure that we have a packet to process.
    if packet_data is None:
        raise ConnectionError("No data received from device")

    # Verify that the device ID is known and has a trusted signature.
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(io_device_id)
    if not expected_signature:
        raise ConnectionError(f"Unknown or untrusted device ID: {io_device_id}")

    # Use constant‑time comparison to mitigate timing attacks (CWE-345).
    if not hmac.compare_digest(crypto_signature.lower(), expected_signature.lower()):
        # Signature does not match – reject the packet.
        return None

    # If we reach this point, the signature is verified successfully.
    return packet_data