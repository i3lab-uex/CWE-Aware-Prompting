import hmac

# Global dictionary mapping device IDs to their expected signatures.
# In a real system this would be stored securely (e.g., in a HSM or encrypted database).
TRUSTED_DEVICE_SIGNATURES = {
    "device_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "device_002": "e99a18c428cb38d5f260853678922e03",
    # Add more device signatures here
}

def process_packet(device_id: str, packet_signature: str, data_packet: dict) -> dict | None:
    """
    Validate the cryptographic signature of an incoming IoT data packet and
    process it if valid.

    Parameters
    ----------
    device_id : str
        Unique identifier of the IoT device sending the packet.
    packet_signature : str
        Cryptographic signature accompanying the packet.
    data_packet : dict
        Payload of the data packet to be processed.

    Returns
    -------
    dict | None
        The original `data_packet` if the signature is valid, otherwise None.

    Raises
    ------
    ConnectionError
        If the packet cannot be received successfully (e.g., `data_packet` is None).
    """
    # Simulate a failure to receive the packet
    if data_packet is None:
        raise ConnectionError("Failed to receive packet from device: %s" % device_id)

    # Retrieve the expected signature for this device
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if expected_sig is None:
        # Unknown device – treat as untrusted
        return None

    # Perform a constant‑time comparison to avoid timing attacks (CWE-693)
    if not hmac.compare_digest(packet_signature, expected_sig):
        # Signature mismatch – packet is not trusted
        return None

    # At this point the signature is valid; perform any additional processing here.
    # For demonstration we simply return the original packet unchanged.
    return data_packet