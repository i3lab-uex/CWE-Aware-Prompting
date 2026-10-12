import hashlib
import hmac
import random

# Global dictionary mapping device IDs to their expected HMAC signatures.
# In a real system this would be securely stored and protected.
TRUSTED_DEVICE_SIGNATURES = {
    "device_001": b"5f4dcc3b5aa765d61d8327deb882cf99",
    "device_002": b"e2fc714c4727ee9395f324cd2e7f331f",
    # Add more device signatures as needed.
}

def _simulate_data_reception() -> None:
    """
    Simulates potential issues when receiving data from an IoT device.
    Randomly raises a ConnectionError to mimic network problems.
    """
    if random.random() < 0.05:  # 5% chance of failure
        raise ConnectionError("Failed to receive data from the IoT device.")

def process_packet_data(id_device: str, packet_signature: str, packet_data: dict):
    """
    Authenticate and process data packets from IoT devices.

    Parameters
    ----------
    id_device : str
        Unique identifier of the device that sent the packet.
    packet_signature : str
        Hex-encoded cryptographic signature attached to the packet.
    packet_data : dict
        Payload of the data packet.

    Returns
    -------
    dict | None
        The original packet_data if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If there was an issue receiving data from the device.
    """
    # Simulate potential reception issues
    _simulate_data_reception()

    # Ensure the device is known
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(id_device)
    if not expected_sig:
        return None  # Unknown device, reject packet

    # Convert the provided signature from hex string to bytes
    try:
        received_sig_bytes = bytes.fromhex(packet_signature)
    except ValueError:
        return None  # Malformed signature

    # Compute a deterministic hash of the packet data for comparison
    # (In practice, use the same algorithm that generated the signature)
    packet_bytes = str(packet_data).encode("utf-8")
    computed_hash = hashlib.sha256(packet_bytes).digest()

    # Use constant-time comparison to mitigate timing attacks
    if hmac.compare_digest(computed_hash, expected_sig):
        return packet_data

    # Signature mismatch
    return None