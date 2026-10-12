import hmac
from typing import Dict, Optional

# Global mapping of trusted device IDs to their expected cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; replace with real values.
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "0j9i8h7g6f5e4d3c2b1a",
    # ...
}

def verify_iot_signature(
    iot_id: str,
    crypto_signature: str,
    packet_info: Dict
) -> Optional[Dict]:
    """
    Validate the cryptographic signature of an IoT data packet.

    Parameters
    ----------
    iot_id : str
        Unique identifier of the IoT device.
    crypto_signature : str
        Cryptographic signature included in the packet.
    packet_info : dict
        The actual data payload of the packet.

    Returns
    -------
    dict or None
        The original `packet_info` if the signature is valid; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the data cannot be retrieved from the IoT device.
    """
    # Simulate a potential network failure when retrieving data
    if packet_info is None:
        raise ConnectionError(f"Failed to receive data from device {iot_id}")

    # Retrieve the expected signature for this device
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(iot_id)
    if expected_sig is None:
        # Unknown device – treat as invalid
        return None

    # Use constant‑time comparison to mitigate timing attacks (CWE‑345)
    if not hmac.compare_digest(crypto_signature, expected_sig):
        return None

    # Signature verified – return the packet data
    return packet_info