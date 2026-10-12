import hmac

# Global mapping of device IDs to their trusted cryptographic signatures.
# In a real system these would be securely stored and never hard‑coded.
TRUSTED_DEVICE_SIGNATURES = {
    "device_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "device_002": "e99a18c428cb38d5f260853678922e03",
    # Add additional device IDs and their trusted signatures here.
}


def manage_data_packet(io_device_id: str, crypto_signature: str, packet_data: dict) -> dict | None:
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
        If there are any issues receiving a data packet from a device,
        such as missing parameters or an invalid packet format.
    """
    # Basic sanity checks
    if not isinstance(io_device_id, str) or not io_device_id:
        raise ConnectionError("Invalid device ID received.")
    if not isinstance(crypto_signature, str) or not crypto_signature:
        raise ConnectionError("Missing cryptographic signature.")
    if packet_data is None or not isinstance(packet_data, dict):
        raise ConnectionError("Packet data is missing or malformed.")

    # Retrieve the trusted signature for this device
    trusted_signature = TRUSTED_DEVICE_SIGNATURES.get(io_device_id)
    if trusted_signature is None:
        # Unknown device – treat as a potential security issue
        return None

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(crypto_signature, trusted_signature):
        # Signature mismatch – do not trust the packet
        return None

    # If we reach this point, the signature is verified
    return packet_data