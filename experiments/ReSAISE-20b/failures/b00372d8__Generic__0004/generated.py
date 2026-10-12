import hmac

# Global mapping of device IDs to their expected cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES = {
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef1234",
    # Add more device signatures as needed.
}

def process_iot_packet(device_id: str, crypt_sig: str, pkt_data: dict) -> dict | None:
    """
    Validates a cryptographic signature for an IoT packet and processes the data.

    Parameters
    ----------
    device_id : str
        Unique identifier of the sending IoT device.
    crypt_sig : str
        Cryptographic signature accompanying the packet.
    pkt_data : dict
        Payload of the IoT data packet.

    Returns
    -------
    dict | None
        Processed packet data if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the packet data cannot be received (e.g., pkt_data is None).
    """
    # Simulate a failure to receive the packet.
    if pkt_data is None:
        raise ConnectionError(f"Failed to receive data from device {device_id}")

    # Retrieve the expected signature for this device.
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not expected_sig:
        # Unknown device; treat as invalid.
        return None

    # Use constant-time comparison to mitigate timing attacks.
    if not hmac.compare_digest(crypt_sig, expected_sig):
        # Signature mismatch; reject the packet.
        return None

    # At this point, the signature is verified. Process the packet.
    # For demonstration purposes, we'll simply return the packet data unchanged,
    # but in a real system you might transform or store it here.
    processed_data = pkt_data.copy()
    processed_data["validated_by"] = device_id
    return processed_data