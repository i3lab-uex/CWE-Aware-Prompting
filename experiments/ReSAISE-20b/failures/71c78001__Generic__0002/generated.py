import json
from typing import Dict, Any

# Global mapping of device IDs to their expected cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef",
    # Add more device signatures as needed.
}

def process_iot_packet(dev_id: str, crypto_sign: str,
                       packet_content: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Authenticate and process an IoT data packet.

    Parameters
    ----------
    dev_id : str
        Unique identifier for the IoT device sending the data.
    crypto_sign : str
        Cryptographic signature attached to the packet.
    packet_content : dict
        The actual content of the packet.

    Returns
    -------
    dict | None
        The packet content if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If an issue occurs while receiving data from the IoT device.
    """
    # Simulate a possible network failure. In real code, this would be
    # triggered by actual I/O exceptions.
    if not isinstance(dev_id, str) or not isinstance(crypto_sign, str):
        raise ConnectionError("Invalid data received from IoT device.")

    # Retrieve the expected signature for this device.
    expected_sign = TRUSTED_DEVICE_SIGNATURES.get(dev_id)
    if not expected_sign:
        # Unknown device: reject the packet.
        return None

    # Verify that the provided signature matches the expected one.
    if crypto_sign != expected_sign:
        return None

    # At this point the packet is authenticated.
    # In a real implementation, additional validation (e.g., JSON schema)
    # and sanitization would be performed here.
    return packet_content