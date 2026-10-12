import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their expected signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries – in production these would be securely stored.
    "device-001": "a3f5c9e7b8d1...",
    "device-002": "4d2a6f9c3b0e...",
    # ...
}

def process_packet(
    device_id: str,
    packet_signature: str,
    data_packet: Optional[Dict]
) -> Optional[Dict]:
    """
    Validate the cryptographic signature of an IoT data packet and return
    the processed payload if validation succeeds.

    Parameters
    ----------
    device_id : str
        Unique identifier of the IoT device.
    packet_signature : str
        Signature string provided with the packet.
    data_packet : dict | None
        The payload to process. If ``None`` the packet is considered lost.

    Returns
    -------
    dict | None
        The processed data if signature verification succeeds; otherwise
        ``None``.

    Raises
    ------
    ConnectionError
        If the packet cannot be received (``data_packet`` is ``None``).
    """
    # Simulate a packet reception failure.
    if data_packet is None:
        raise ConnectionError(f"Failed to receive packet from device {device_id}")

    # Retrieve the expected signature for this device.
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not expected_sig:
        # Unknown device – reject silently.
        return None

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(packet_signature, expected_sig):
        # Signature mismatch – reject.
        return None

    # At this point the packet is authenticated; perform any
    # domain‑specific processing here.  For illustration, we simply
    # return the payload unchanged.
    processed_data = data_packet.copy()
    return processed_data