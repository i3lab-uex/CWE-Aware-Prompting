import hmac
import hashlib

# Global dictionary mapping device IDs to their expected signatures.
TRUSTED_DEVICE_SIGNATURES = {
    # Example entries (replace with real values)
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef1234",
}

def _constant_time_compare(val1: str, val2: str) -> bool:
    """
    Compare two strings in constant time to mitigate timing attacks.
    Uses hmac.compare_digest under the hood.
    """
    return hmac.compare_digest(val1.encode("utf-8"), val2.encode("utf-8"))

def process_packet(device_id: str, packet_signature: str, data_packet: dict):
    """
    Validate the authenticity of a data packet from an IoT device and
    process it if the signature is correct.

    Parameters:
        device_id (str): Unique identifier of the sending IoT device.
        packet_signature (str): Cryptographic signature accompanying the packet.
        data_packet (dict): Payload to be processed.

    Returns:
        dict: The processed data if validation succeeds.
        None: If the signature does not match or the device is unknown.

    Raises:
        ConnectionError: If the packet cannot be received (e.g., data_packet is None).
    """
    # Ensure we actually received a packet.
    if data_packet is None:
        raise ConnectionError("Packet could not be received.")

    # Verify that the device ID is known.
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not expected_sig:
        # Unknown device: treat as unauthenticated.
        return None

    # Perform a constant‑time comparison of the provided and expected signatures.
    if not _constant_time_compare(packet_signature, expected_sig):
        # Signature mismatch: do not process.
        return None

    # At this point the packet is authenticated.  Perform minimal
    # processing; in a real system you would add domain‑specific logic here.
    processed_data = {
        "device_id": device_id,
        "timestamp": data_packet.get("timestamp"),
        "payload": data_packet.get("payload"),
    }
    return processed_data