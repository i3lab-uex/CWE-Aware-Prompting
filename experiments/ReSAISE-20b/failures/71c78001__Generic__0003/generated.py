import hmac
from typing import Dict, Optional

# Global registry of trusted device signatures.
# In a real system this would be populated from secure storage or a database.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    "device_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "device_002": "6b86b273ff34fce19d6b804eff5a3f57",
    # Add more device IDs and their expected signatures here.
}


def process_iot_packet(
    dev_id: str,
    crypto_sign: str,
    packet_content: Dict
) -> Optional[Dict]:
    """
    Authenticate and process an IoT data packet.

    Parameters
    ----------
    dev_id : str
        Unique identifier of the sending IoT device.
    crypto_sign : str
        Cryptographic signature attached to the packet.
    packet_content : dict
        The actual payload of the packet.

    Returns
    -------
    dict | None
        The packet content if authentication succeeds; otherwise `None`.

    Raises
    ------
    ConnectionError
        If the device is unknown or its signature cannot be retrieved.
    """
    # Validate input types
    if not isinstance(dev_id, str):
        raise TypeError("dev_id must be a string")
    if not isinstance(crypto_sign, str):
        raise TypeError("crypto_sign must be a string")
    if not isinstance(packet_content, dict):
        raise TypeError("packet_content must be a dictionary")

    # Retrieve the expected signature for this device.
    try:
        expected_sign = TRUSTED_DEVICE_SIGNATURES[dev_id]
    except KeyError as exc:
        # Treat an unknown device as a connection/identification error.
        raise ConnectionError(f"Unknown device ID: {dev_id}") from exc

    # Compare signatures in constant time to mitigate timing attacks.
    if not hmac.compare_digest(expected_sign, crypto_sign):
        # Signature mismatch – data is considered untrusted.
        return None

    # At this point the packet is authenticated; we can safely return it.
    return packet_content