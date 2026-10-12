import hmac
import hashlib
import datetime

# Global dictionary mapping device IDs to their expected cryptographic signatures.
# In a real deployment this would be securely stored and rotated as needed.
TRUSTED_DEVICE_SIGNATURES = {
    "device_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "device_002": "e99a18c428cb38d5f260853678922e03",
    # ... add more device signatures here ...
}

def _verify_signature(device_id: str, provided_sig: str) -> bool:
    """
    Verify that the provided signature matches the expected one for the device.
    Uses constant‑time comparison to mitigate timing attacks.
    """
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if expected_sig is None:
        return False
    # Ensure both signatures are byte strings for compare_digest
    return hmac.compare_digest(
        expected_sig.encode('utf-8'),
        provided_sig.encode('utf-8')
    )

def _process_data(packet: dict) -> dict:
    """
    Perform minimal processing on the data packet.
    For demonstration, we simply add a processed timestamp.
    """
    processed = dict(packet)  # shallow copy to avoid mutating the original
    processed["processed_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    return processed

def process_packet(device_id: str, packet_signature: str, data_packet: dict) -> dict | None:
    """
    Validate and process a packet from an IoT device.

    Parameters
    ----------
    device_id : str
        Unique identifier of the sending IoT device.
    packet_signature : str
        Cryptographic signature accompanying the packet.
    data_packet : dict
        Payload of the packet to be processed.

    Returns
    -------
    dict | None
        The processed data if signature validation succeeds, otherwise None.

    Raises
    ------
    ConnectionError
        If the packet cannot be received successfully.
    """
    # In a real scenario, this is where you'd check network conditions or
    # catch lower‑level exceptions. Here we simulate a potential failure.
    if data_packet is None:
        raise ConnectionError(f"Failed to receive packet from device {device_id}")

    if not _verify_signature(device_id, packet_signature):
        # Signature does not match; do not process the packet.
        return None

    # All checks passed – proceed to process the data.
    return _process_data(data_packet)