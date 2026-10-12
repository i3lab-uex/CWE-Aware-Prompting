import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their expected HMAC signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; in production these would be securely stored.
    "device-001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "device-002": "6cb75f9b5c8d6e4a1d3f2e7b9a0c1e5d",
    # ...
}

def process_packet(
    device_id: str,
    packet_signature: str,
    data_packet: Dict
) -> Optional[Dict]:
    """
    Validates the cryptographic signature of a data packet from an IoT device
    and processes the packet if validation succeeds.

    Parameters
    ----------
    device_id : str
        Unique identifier of the sending IoT device.
    packet_signature : str
        Cryptographic signature included with the packet.
    data_packet : dict
        The payload of the packet to process.

    Returns
    -------
    Optional[Dict]
        Processed data dictionary if signature is valid, otherwise None.

    Raises
    ------
    ConnectionError
        If the packet cannot be received (simulated by an empty payload).
    """

    # Simulate a failure to receive the packet.
    if data_packet is None:
        raise ConnectionError("Packet could not be received from device.")

    # Ensure the device is known.
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if expected_sig is None:
        # Unknown device; treat as untrusted.
        return None

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(packet_signature, expected_sig):
        # Signature mismatch; reject packet.
        return None

    # If signature is valid, proceed with processing.
    # (Processing logic would be device‑specific; here we simply return the data.)
    processed_data = {
        "device_id": device_id,
        **data_packet
    }
    return processed_data