import hashlib
from typing import Dict, Optional

# Global mapping of device IDs to their expected cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    "device-001": "5f4dcc3b5aa765d61d8327deb882cf99",  # example MD5 hash
    "device-002": "e99a18c428cb38d5f260853678922e03",
    # Add more trusted device signatures here.
}

def _simulate_data_reception(iot_id: str) -> None:
    """
    Simulate potential failures when receiving data from an IoT device.
    In a real implementation this would involve network I/O and could raise
    ConnectionError if the device is unreachable or the connection times out.
    """
    # For demonstration, raise ConnectionError if the device ID is not known
    # or if a random condition occurs.
    if iot_id not in TRUSTED_DEVICE_SIGNATURES:
        raise ConnectionError(f"Unable to reach device {iot_id}")

def verify_iot_signature(
    iot_id: str,
    crypto_signature: str,
    packet_info: Dict
) -> Optional[Dict]:
    """
    Verify the cryptographic signature of an IoT data packet and return
    the packet content if it is authentic.

    Parameters:
        iot_id (str): Unique identifier of the IoT device.
        crypto_signature (str): Signature attached to the data packet.
        packet_info (dict): The actual content of the packet.

    Returns:
        dict: The packet content if the signature is valid.
        None: If the signature does not match.

    Raises:
        ConnectionError: If there is an issue receiving data from the device.
    """
    # Simulate a network/data reception step that might fail
    _simulate_data_reception(iot_id)

    # Retrieve the expected signature for this device
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(iot_id)
    if expected_sig is None:
        # Device not trusted
        return None

    # For security, compare signatures using a constant‑time comparison
    if not _constant_time_compare(crypto_signature, expected_sig):
        return None

    # Signature is valid; return the packet data
    return packet_info


def _constant_time_compare(val1: str, val2: str) -> bool:
    """
    Compare two strings in constant time to prevent timing attacks.
    """
    if len(val1) != len(val2):
        return False
    result = 0
    for x, y in zip(val1.encode(), val2.encode()):
        result |= x ^ y
    return result == 0