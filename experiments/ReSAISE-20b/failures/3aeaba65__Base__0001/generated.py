import hmac

# Global mapping of trusted device IDs to their expected signatures.
TRUSTED_DEVICE_SIGNATURES = {
    # Example entries:
    # "device_123": "a1b2c3d4e5f6...",
    # ...
}


def verify_iot_signature(iot_id: str, crypto_signature: str, packet_info: dict) -> dict | None:
    """
    Validate the cryptographic signature of an IoT data packet.

    Parameters
    ----------
    iot_id : str
        Unique identifier of the IoT device sending the packet.
    crypto_signature : str
        Cryptographic signature attached to the data packet.
    packet_info : dict
        The actual content of the packet to be processed.

    Returns
    -------
    dict | None
        The original `packet_info` if the signature is valid; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the device is unknown or if no signature is provided.
    """
    # Ensure we have a known device
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(iot_id)
    if expected_signature is None:
        raise ConnectionError(f"Unknown IoT device: {iot_id}")

    # Ensure a signature was provided
    if not crypto_signature:
        raise ConnectionError(f"No signature received from device {iot_id}")

    # Use constant‑time comparison to prevent timing attacks
    if hmac.compare_digest(crypto_signature, expected_signature):
        return packet_info

    # Signature did not match
    return None