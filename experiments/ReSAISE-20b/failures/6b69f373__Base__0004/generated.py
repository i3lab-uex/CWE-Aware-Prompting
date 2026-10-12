import json
import hmac
import hashlib

# Global dictionary mapping device IDs to their secret keys (HMAC keys)
TRUSTED_DEVICE_SIGNATURES = {
    # Example entries – in production these would be securely stored
    "device-001": b"supersecretkey123",
    "device-002": b"anotherverysecretkey456",
}

def _compute_hmac(key: bytes, message: str) -> str:
    """
    Compute an HMAC-SHA256 hex digest for the given message using the provided key.
    """
    return hmac.new(key, message.encode("utf-8"), hashlib.sha256).hexdigest()

def validate_device_packet(iot_device_id: str, iot_signature: str, iot_data: dict) -> dict | None:
    """
    Validate the cryptographic signature of an IoT device packet and return the
    processed data if validation succeeds.

    Parameters:
        iot_device_id (str): Unique identifier of the sending device.
        iot_signature (str): Hex-encoded signature accompanying the packet.
        iot_data (dict): The data payload to validate.

    Returns:
        dict | None: Processed data dictionary if signature is valid; otherwise None.

    Raises:
        ConnectionError: If the packet cannot be received (e.g., missing data).
    """
    # Simulate a potential receive failure
    if iot_data is None:
        raise ConnectionError(f"Packet from device '{iot_device_id}' could not be received.")

    # Ensure the device is trusted
    secret_key = TRUSTED_DEVICE_SIGNATURES.get(iot_device_id)
    if not secret_key:
        # Unknown device – treat as untrusted
        return None

    # Canonicalize the data to a JSON string with sorted keys for deterministic signing
    try:
        canonical_payload = json.dumps(iot_data, separators=(",", ":"), sort_keys=True)
    except (TypeError, ValueError) as exc:
        # Payload cannot be serialized – treat as invalid
        return None

    # Compute the expected HMAC signature
    expected_signature = _compute_hmac(secret_key, canonical_payload)

    # Constant-time comparison to mitigate timing attacks
    if not hmac.compare_digest(expected_signature, iot_signature.lower()):
        # Signature mismatch – reject packet
        return None

    # At this point the signature is valid; process data as needed.
    # For demonstration, we simply return the original dictionary.
    processed_data = iot_data.copy()
    # Additional processing steps could be inserted here.

    return processed_data