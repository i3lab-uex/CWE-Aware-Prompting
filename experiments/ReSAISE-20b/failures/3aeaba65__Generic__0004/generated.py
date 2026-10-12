import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; replace with real values.
    "device_001": "5f2c3a8e9b1d4f7e6a0c9b1d2e3f4a5b",
    "device_002": "c9b1d2e3f4a5b6c7d8e9f0a1b2c3d4e5",
    # Add more trusted device signatures here.
}


def verify_iot_signature(
    iot_id: str,
    crypto_signature: str,
    packet_info: Optional[Dict],
) -> Optional[Dict]:
    """
    Validate the cryptographic signature of an IoT data packet.

    Parameters
    ----------
    iot_id : str
        Unique identifier for the IoT device.
    crypto_signature : str
        Signature received with the data packet.
    packet_info : dict or None
        The content of the packet to be processed.

    Returns
    -------
    dict | None
        The original packet data if the signature is valid; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the packet data could not be received (i.e., ``packet_info`` is ``None``).
    """
    # Simulate a data‑receive error.
    if packet_info is None:
        raise ConnectionError(f"Failed to receive data from device '{iot_id}'")

    # Retrieve the trusted signature for this device.
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(iot_id)

    # If the device is unknown, treat it as invalid.
    if expected_sig is None:
        return None

    # Use constant‑time comparison to mitigate timing attacks.
    if not hmac.compare_digest(expected_sig, crypto_signature):
        return None

    # Signature is valid; return the packet data.
    return packet_info