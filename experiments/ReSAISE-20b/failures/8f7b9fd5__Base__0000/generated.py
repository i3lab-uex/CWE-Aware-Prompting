import hmac
import hashlib
import json

# Global dictionary mapping device IDs to their shared secret keys.
TRUSTED_DEVICE_SIGNATURES = {
    # Example entries (device_id: shared_secret)
    "device_001": b"supersecretkey1",
    "device_002": b"anothersecretkey2",
    # Add more device mappings here
}


def _compute_hmac(secret: bytes, data: dict) -> str:
    """
    Compute a hex-encoded HMAC-SHA256 of the given data dictionary.
    The data is first serialized to JSON with sorted keys to ensure
    deterministic ordering.

    Args:
        secret (bytes): The shared secret key for HMAC.
        data (dict): The payload to sign.

    Returns:
        str: Hexadecimal representation of the HMAC digest.
    """
    # Serialize with sorted keys for deterministic output
    serialized = json.dumps(data, separators=(",", ":"), sort_keys=True).encode("utf-8")
    mac = hmac.new(secret, serialized, hashlib.sha256)
    return mac.hexdigest()


def process_packet(device_id: str, packet_signature: str, data_packet: dict):
    """
    Validate the cryptographic signature of an IoT device's data packet and
    return the processed data if verification succeeds.

    Args:
        device_id (str): Unique identifier of the IoT device.
        packet_signature (str): Hex-encoded signature sent with the packet.
        data_packet (dict): The content of the data packet.

    Returns:
        dict | None: Processed data if signature is valid; otherwise None.

    Raises:
        ConnectionError: If the packet cannot be received (e.g., data_packet is None).
    """
    # Simulate a failure to receive the packet
    if data_packet is None:
        raise ConnectionError(f"Failed to receive packet from device {device_id}")

    # Retrieve the shared secret for this device
    secret = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if secret is None:
        # Unknown device – treat as invalid
        return None

    # Compute expected signature
    try:
        expected_sig = _compute_hmac(secret, data_packet)
    except Exception as e:
        # Any error during HMAC calculation should be treated as a failure
        return None

    # Constant-time comparison to mitigate timing attacks (CWE-347)
    if not hmac.compare_digest(expected_sig, packet_signature):
        return None

    # At this point the signature is verified – process and return data
    # (Processing logic would go here; for now we simply echo the packet)
    return data_packet