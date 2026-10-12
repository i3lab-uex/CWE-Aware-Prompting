import hashlib
import hmac
import os
import random

# Global trusted signatures mapping device_id -> secret key (hex string)
TRUSTED_DEVICE_SIGNATURES = {
    # Example: device_id : secret_key
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "deadbeefcafebabe1234",
}

def _receive_packet(iot_device_id: str, iot_data: dict) -> bool:
    """
    Simulate packet reception. Randomly fail to emulate network issues.
    Returns True if the packet is considered successfully received.
    """
    # 5% chance of failure
    return random.random() > 0.05

def _verify_signature(
    device_id: str,
    signature_hex: str,
    data: dict
) -> bool:
    """
    Verify the HMAC-SHA256 signature of the data using a secret key
    stored in TRUSTED_DEVICE_SIGNATURES. The data dict is serialized
    into a canonical JSON string (sorted keys) before hashing.
    """
    if device_id not in TRUSTED_DEVICE_SIGNATURES:
        return False

    secret_key = TRUSTED_DEVICE_SIGNATURES[device_id].encode()
    # Canonical JSON representation
    data_bytes = (
        bytes(str(sorted(data.items())), "utf-8")
    )  # simple deterministic serialization

    computed_hmac = hmac.new(secret_key, data_bytes, hashlib.sha256).hexdigest()
    # Constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(computed_hmac, signature_hex)

def validate_device_packet(
    iot_device_id: str,
    iot_signature: str,
    iot_data: dict
) -> dict | None:
    """
    Validate the authenticity of a packet from an IoT device.

    Parameters
    ----------
    iot_device_id : str
        Unique identifier of the sending device.
    iot_signature : str
        Hexadecimal HMAC‑SHA256 signature accompanying the packet.
    iot_data : dict
        The payload to be processed.

    Returns
    -------
    dict | None
        Processed data if verification succeeds, otherwise None.

    Raises
    ------
    ConnectionError
        If the packet cannot be received (simulated network failure).
    """
    # 1. Ensure the packet was successfully received
    if not _receive_packet(iot_device_id, iot_data):
        raise ConnectionError(f"Failed to receive packet from {iot_device_id}")

    # 2. Verify signature authenticity
    if not _verify_signature(iot_device_id, iot_signature, iot_data):
        return None

    # 3. Process data (placeholder for actual business logic)
    processed = iot_data.copy()
    processed["validated_at"] = os.urandom(8).hex()  # example metadata

    return processed