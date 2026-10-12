import hmac
import hashlib
from typing import Dict, Optional

# Global mapping of device IDs to the expected cryptographic signatures.
# In a real system this would be stored securely (e.g., in a vault).
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (device_id : expected_signature)
    "device_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "device_002": "e99a18c428cb38d5f260853678922e03",
    # Add more device signatures as needed.
}


def verify_iot_signature(
    iot_id: str,
    crypto_signature: str,
    packet_info: Dict
) -> Optional[Dict]:
    """
    Validate a cryptographic signature from an IoT device and return the packet data.

    Parameters
    ----------
    iot_id : str
        Unique identifier for the IoT device.
    crypto_signature : str
        The cryptographic signature attached to the data packet.
    packet_info : dict
        The actual content of the packet.

    Returns
    -------
    dict | None
        The packet data if signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If data could not be received from the IoT device.
    """
    # Simulate a connectivity issue if packet_info is None
    if packet_info is None:
        raise ConnectionError(f"Failed to receive data from device {iot_id}")

    # Retrieve the expected signature for this device
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(iot_id)
    if expected_signature is None:
        # Unknown device – treat as a potential attack
        return None

    # Use constant‑time comparison to prevent timing attacks (CWE‑693)
    if not hmac.compare_digest(crypto_signature, expected_signature):
        return None

    # Signature is valid – return the packet data
    return packet_info