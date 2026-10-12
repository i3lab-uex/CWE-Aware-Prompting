import hmac
from typing import Dict, Optional

# Global dictionary mapping device IDs to their expected cryptographic signatures.
# In a real system this would be securely stored and not hard‑coded.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    "device-001": "a1b2c3d4e5f6g7h8i9j0",
    "device-002": "b2c3d4e5f6g7h8i9j0a1",
    # ... add more trusted devices here
}

def process_iot_packet(
    device_id: str,
    crypt_sig: str,
    pkt_data: Optional[Dict],
) -> Optional[Dict]:
    """
    Validate the cryptographic signature of an IoT packet and process its data.

    Parameters
    ----------
    device_id : str
        Unique identifier of the sending IoT device.
    crypt_sig : str
        Cryptographic signature accompanying the packet.
    pkt_data : dict | None
        The content of the data packet to be processed.

    Returns
    -------
    dict | None
        The processed data dictionary if signature verification succeeds,
        otherwise ``None``. A :class:`ConnectionError` is raised if the
        packet cannot be received (i.e., ``pkt_data`` is ``None``).

    Raises
    ------
    ConnectionError
        If the packet data cannot be received (``pkt_data`` is ``None``).
    """
    # Ensure the packet was received successfully.
    if pkt_data is None:
        raise ConnectionError("Failed to receive packet from device.")

    # Retrieve the expected signature for this device.
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if expected_sig is None:
        # Device not recognized; reject the packet.
        return None

    # Use a constant‑time comparison to avoid timing attacks (CWE-693).
    if not hmac.compare_digest(crypt_sig, expected_sig):
        return None

    # At this point the packet is authenticated.
    # Perform any device‑specific processing here. For illustration,
    # we simply return the packet data unchanged.
    processed_data = dict(pkt_data)  # shallow copy to avoid side effects
    return processed_data