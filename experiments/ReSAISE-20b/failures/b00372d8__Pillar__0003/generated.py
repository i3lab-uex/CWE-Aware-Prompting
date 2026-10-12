import hmac
import hashlib
from typing import Dict, Any

# Global mapping of device IDs to their expected cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; replace with actual values in production.
    "device_001": "a1b2c3d4e5f67890",
    "device_002": "0f1e2d3c4b5a6978",
}

def process_iot_packet(device_id: str, crypt_sig: str, pkt_data: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Validate the cryptographic signature of an IoT packet and return the processed data.

    Parameters
    ----------
    device_id : str
        Unique identifier of the sending IoT device.
    crypt_sig : str
        Cryptographic signature accompanying the packet.
    pkt_data : dict
        The content of the data packet to be processed.

    Returns
    -------
    dict or None
        The processed packet data if the signature is valid; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the packet data cannot be received (i.e., ``pkt_data`` is None).
    """
    # Simulate a failure to receive the packet.
    if pkt_data is None:
        raise ConnectionError(f"Failed to receive packet from device {device_id}")

    # Retrieve the expected signature for this device.
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not expected_sig:
        # Unknown device – treat as an invalid packet.
        return None

    # Perform a timing‑attack resistant comparison of signatures.
    if not hmac.compare_digest(expected_sig, crypt_sig):
        # Signature mismatch – reject the packet.
        return None

    # At this point, the signature is verified. Process the packet data as needed.
    # For demonstration purposes we simply return the packet unchanged,
    # but real implementations might transform, validate, or store it.
    processed_data = dict(pkt_data)  # shallow copy to avoid side‑effects
    return processed_data