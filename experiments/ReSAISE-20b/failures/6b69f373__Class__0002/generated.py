import hmac
import hashlib

# Example trusted signatures mapping.
# In production this would be securely stored and not hard‑coded.
TRUSTED_DEVICE_SIGNATURES = {
    # device_id: signature (hex string)
    "device-001": "a1b2c3d4e5f67890123456789abcdef0",
    "device-002": "1234567890abcdef1234567890abcdef",
    # add more devices as needed
}


def validate_device_packet(iot_device_id: str,
                           iot_signature: str,
                           iot_data: dict) -> dict | None:
    """
    Validate the cryptographic signature of an IoT device packet and return
    the processed data if authentication succeeds.

    Parameters
    ----------
    iot_device_id : str
        Unique identifier of the IoT device.
    iot_signature : str
        Hexadecimal string representing the signature sent by the device.
    iot_data : dict
        The data payload received from the device.

    Returns
    -------
    dict | None
        The processed data dictionary if signature validation passes;
        otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the packet cannot be received successfully (e.g., data is None).
    """
    # 1. Ensure the packet was received
    if iot_data is None:
        raise ConnectionError("Failed to receive data packet from device "
                               f"'{iot_device_id}'.")
    if not isinstance(iot_data, dict):
        # Reject non‑dict payloads to avoid unexpected behavior
        return None

    # 2. Retrieve the trusted signature for this device
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(iot_device_id)
    if not expected_sig:
        # Unknown device: reject silently
        return None

    # 3. Perform a constant‑time comparison to prevent timing attacks
    try:
        # Convert signatures from hex strings to bytes for compare_digest
        expected_bytes = bytes.fromhex(expected_sig)
        provided_bytes = bytes.fromhex(iot_signature)
    except ValueError:
        # Malformed signature format
        return None

    if not hmac.compare_digest(provided_bytes, expected_bytes):
        # Signature mismatch
        return None

    # 4. At this point, authentication succeeded; process the data.
    # For demonstration we simply return the payload unchanged.
    # Real implementations would parse, validate fields, etc.
    return iot_data