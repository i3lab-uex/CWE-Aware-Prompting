import hmac
import hashlib
from datetime import datetime

# Example trusted signatures dictionary (device_id -> hex digest)
TRUSTED_DEVICE_SIGNATURES = {
    "sensor_01": "5f4dcc3b5aa765d61d8327deb882cf99",
    "sensor_02": "e99a18c428cb38d5f260853678922e03",
    # Add more device IDs and their expected signatures here
}


def _verify_signature(device_id: str, signature: str) -> bool:
    """
    Securely compare the provided signature with the expected one using
    constant‑time comparison to mitigate timing attacks.
    """
    expected = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if expected is None:
        return False
    # Ensure both signatures are bytes for hmac.compare_digest
    return hmac.compare_digest(
        signature.encode("utf-8"),
        expected.encode("utf-8")
    )


def process_packet(device_id: str, packet_signature: str, data_packet: dict):
    """
    Validate the cryptographic signature of a packet from an IoT device and
    return the processed data if valid.

    Parameters:
        device_id (str): Unique identifier of the IoT device.
        packet_signature (str): Signature accompanying the data packet.
        data_packet (dict): The actual payload to be processed.

    Returns:
        dict: The processed data if the signature is valid.
        None: If the signature validation fails.

    Raises:
        ConnectionError: If the packet cannot be received (e.g., data_packet is None).
    """
    if data_packet is None:
        raise ConnectionError("Failed to receive packet from device: payload missing.")

    if not _verify_signature(device_id, packet_signature):
        return None

    # Example processing: add a timestamp and device ID to the payload
    processed = dict(data_packet)  # shallow copy to avoid side effects
    processed["received_at"] = datetime.utcnow().isoformat() + "Z"
    processed["device_id"] = device_id

    return processed