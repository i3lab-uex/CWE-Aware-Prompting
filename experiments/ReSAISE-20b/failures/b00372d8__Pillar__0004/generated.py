import hmac
import hashlib

# Global mapping of device IDs to their expected cryptographic signatures.
# In a real system these would be secure secrets (e.g., HMAC keys).
TRUSTED_DEVICE_SIGNATURES = {
    "device_001": "a3f4e2c1b5d7",
    "device_002": "9b8c7d6e5f4a",
    # Add more device signatures as needed.
}

def _receive_packet(device_id: str) -> bool:
    """
    Simulates the reception of a packet from an IoT device.
    In production, this would involve network I/O and error handling.
    Returns True if the packet is received successfully; otherwise False.
    """
    # Placeholder for actual network logic. Assume success here.
    return True

def process_iot_packet(device_id: str, crypt_sig: str, pkt_data: dict) -> dict | None:
    """
    Validates a cryptographic signature for an IoT packet and processes the data.

    Args:
        device_id (str): Unique identifier for the IoT device.
        crypt_sig (str): Cryptographic signature accompanying the packet.
        pkt_data (dict): Payload of the data packet.

    Returns:
        dict | None: The processed data if signature validation succeeds; otherwise None.

    Raises:
        ConnectionError: If the packet cannot be received successfully.
    """
    # Step 1: Verify that the packet is received before any processing.
    if not _receive_packet(device_id):
        raise ConnectionError(f"Failed to receive packet from device {device_id}")

    # Step 2: Ensure the device is known and has a trusted signature.
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if expected_sig is None:
        # Unknown device – treat as untrusted.
        return None

    # Step 3: Validate the cryptographic signature using a constant‑time comparison
    # to mitigate timing attacks (CWE-693).
    if not isinstance(crypt_sig, str):
        return None

    # Use HMAC with SHA256 for demonstration; in practice the signing algorithm
    # must match what the device uses. The expected signature is assumed to be
    # the hex digest of an HMAC keyed with a shared secret.
    try:
        # Derive the expected HMAC from the packet data using the known key.
        # For simplicity, assume the shared secret is the expected signature itself.
        key = expected_sig.encode("utf-8")
        msg = str(pkt_data).encode("utf-8")  # deterministic serialization
        hmac_obj = hmac.new(key, msg, hashlib.sha256)
        computed_sig = hmac_obj.hexdigest()
    except Exception:
        # If any error occurs during HMAC computation, reject the packet.
        return None

    # Constant‑time comparison to avoid leaking information via timing differences.
    if not hmac.compare_digest(computed_sig, crypt_sig):
        return None

    # Step 4: Process the packet data.
    # In a real implementation, this might involve validation, transformation,
    # or storage. Here we simply return the data unchanged.
    processed_data = pkt_data.copy()
    # Example processing: add a timestamp of receipt
    from datetime import datetime, timezone
    processed_data["received_at"] = datetime.now(timezone.utc).isoformat()
    return processed_data