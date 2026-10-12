import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their trusted cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, bytes] = {
    # Example entries; in a real system these would be securely stored.
    "device_001": b"\x12\x34\x56\x78\x9a\xbc\xde\xf0",
    "device_002": b"\xaa\xbb\xcc\xdd\xee\xff\x00\x11",
}

def handle_data_packet(device_id: str, signature: str, data: Dict) -> Optional[Dict]:
    """
    Process a data packet from an IoT device after verifying its signature.

    Args:
        device_id (str): The identification number of the IoT device that sent the data.
        signature (str): The cryptographic signature accompanying the packet, encoded as a hex string.
        data (dict): The payload of the packet that needs to be processed.

    Returns:
        dict | None: The data dictionary if the signature is valid, otherwise None.

    Raises:
        ConnectionError: If the data packet is not received properly (e.g., missing or malformed).
    """
    # Basic sanity checks for packet integrity
    if data is None:
        raise ConnectionError("Data packet not received or corrupted.")
    if not isinstance(data, dict):
        raise ConnectionError("Data payload must be a dictionary.")

    # Retrieve the trusted signature for this device
    trusted_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not trusted_sig:
        # Unknown device – treat as untrusted
        return None

    try:
        # Convert the provided signature from hex to bytes
        provided_sig = bytes.fromhex(signature)
    except ValueError:
        # Signature is not valid hex
        return None

    # Constant‑time comparison to mitigate timing attacks (CWE-345 related)
    if not hmac.compare_digest(provided_sig, trusted_sig):
        return None

    # If we reach this point, the signature is valid and data can be trusted
    return data