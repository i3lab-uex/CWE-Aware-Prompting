import hmac

# Global mapping of device IDs to their trusted cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES = {
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "0123456789abcdef1234",
    # Add more device signatures as needed.
}

def handle_data_packet(device_id: str, signature: str, data: dict) -> dict | None:
    """
    Process a data packet from an IoT device after verifying its signature.

    Args:
        device_id: The identification number of the IoT device that sent the data.
        signature: The cryptographic signature accompanying the packet.
        data: The payload of the packet that needs to be processed.

    Returns:
        The original `data` dictionary if the signature is valid.
        None if the signature does not match a trusted value.

    Raises:
        ConnectionError: If the data packet is missing or malformed.
    """
    # Basic validation of input arguments
    if device_id is None or signature is None:
        raise ConnectionError("Data packet missing required fields")

    if not isinstance(data, dict):
        raise ConnectionError("Malformed data: payload is not a dictionary")

    # Retrieve the trusted signature for this device, if any
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if expected_signature is None:
        # Unknown device; treat as untrusted
        return None

    # Perform a constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(signature, expected_signature):
        return None

    # Signature verified – return the data as-is
    return data