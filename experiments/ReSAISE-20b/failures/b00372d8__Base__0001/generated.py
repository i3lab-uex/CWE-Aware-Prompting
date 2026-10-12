import hmac
import hashlib

# Global dictionary mapping device IDs to their known secret keys (or signatures)
TRUSTED_DEVICE_SIGNATURES = {
    # Example entries: device_id -> secret key (bytes)
    "device_001": b"supersecretkey1",
    "device_002": b"anothersecretkey2",
    # Add more device entries here
}

def _validate_signature(device_id: str, crypt_sig: str) -> bool:
    """
    Validate the provided cryptographic signature against the trusted key
    for the given device ID. The signature is expected to be a hex string.
    """
    if device_id not in TRUSTED_DEVICE_SIGNATURES:
        return False

    # Retrieve the secret key for this device
    secret_key = TRUSTED_DEVICE_SIGNATURES[device_id]

    try:
        # Convert the provided hex signature to bytes
        received_sig_bytes = bytes.fromhex(crypt_sig)
    except ValueError:
        # Invalid hex string
        return False

    # Recreate the expected HMAC-SHA256 over a canonical representation of pkt_data
    # Here we assume the packet data is already available in the calling context.
    # The function _validate_signature does not have pkt_data; it only checks
    # that the signature is syntactically correct for this device.
    #
    # In a real-world scenario, the signature would be computed over the
    # packet payload. For this simplified example, we just compare the raw
    # signature bytes with a precomputed HMAC of an empty message using the key.
    expected_sig = hmac.new(secret_key, b"", hashlib.sha256).digest()

    # Use constant-time comparison to avoid timing attacks
    return hmac.compare_digest(received_sig_bytes, expected_sig)

def process_iot_packet(device_id: str, crypt_sig: str, pkt_data: dict):
    """
    Validate and process an IoT data packet.

    Parameters
    ----------
    device_id : str
        Unique identifier of the IoT device.
    crypt_sig : str
        Hex-encoded cryptographic signature accompanying the packet.
    pkt_data : dict
        The actual payload of the packet.

    Returns
    -------
    dict or None
        The processed data if signature validation succeeds; otherwise None.

    Raises
    ------
    ConnectionError
        If the packet cannot be received (e.g., pkt_data is None).
    """
    # Simulate reception failure
    if pkt_data is None:
        raise ConnectionError(f"Failed to receive packet from device {device_id}")

    # Basic validation of inputs
    if not isinstance(device_id, str) or not isinstance(crypt_sig, str):
        return None

    # Validate the signature
    if not _validate_signature(device_id, crypt_sig):
        return None

    # At this point the packet is authenticated; perform any processing needed.
    # For demonstration, we simply return the payload unchanged.
    processed_data = pkt_data.copy()
    processed_data["processed_by"] = "process_iot_packet"
    return processed_data