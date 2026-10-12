import hmac
from datetime import datetime

# Global dictionary mapping device IDs to their expected cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES = {
    # Example entries; in a real system these would be securely stored.
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef",
}

def process_packet(device_id: str, packet_signature: str, data_packet: dict) -> dict | None:
    """
    Validate and process an IoT device packet.

    Parameters
    ----------
    device_id : str
        Unique identifier of the sending IoT device.
    packet_signature : str
        Cryptographic signature accompanying the data packet.
    data_packet : dict
        The content of the data packet to be processed.

    Returns
    -------
    dict | None
        The processed data dictionary if validation succeeds; otherwise, None.

    Raises
    ------
    ConnectionError
        If the packet could not be received successfully.
    TypeError
        If `data_packet` is not a dictionary.
    """
    # Ensure the packet payload is a dictionary
    if not isinstance(data_packet, dict):
        raise TypeError("data_packet must be a dictionary")

    # Simulate a receipt check – in real usage this would come from the transport layer
    if not data_packet.get("received", True):
        raise ConnectionError(f"Packet from device {device_id} could not be received.")

    # Retrieve the expected signature for this device
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if expected_sig is None:
        # Unknown device – reject
        return None

    # Constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(packet_signature, expected_sig):
        return None

    # Process the packet (example: add a processed flag and timestamp)
    processed_packet = data_packet.copy()
    processed_packet["processed"] = True
    processed_packet["processed_at"] = datetime.utcnow().isoformat() + "Z"

    return processed_packet