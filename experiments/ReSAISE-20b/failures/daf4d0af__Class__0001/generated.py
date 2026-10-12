import hmac
from typing import Dict, Optional

# Global mapping of trusted device IDs to their expected signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; replace with actual trusted signatures.
    "device_001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "device_002": "e99a18c428cb38d5f260853678922e03",
}

def handle_data_packet(device_id: str, signature: str, data: Dict) -> Optional[Dict]:
    """
    Process a data packet from an IoT device after verifying its cryptographic signature.

    Args:
        device_id (str): Identifier of the IoT device that sent the packet.
        signature (str): Cryptographic signature accompanying the packet.
        data (dict): Payload of the packet to be processed.

    Returns:
        dict: The original data dictionary if the signature is valid.
        None: If the signature does not match or the device ID is untrusted.

    Raises:
        ConnectionError: If the packet is malformed (e.g., missing data or invalid type).
    """
    # Validate input types and presence
    if not isinstance(device_id, str) or not isinstance(signature, str):
        raise ConnectionError("Invalid packet metadata received.")
    if data is None or not isinstance(data, dict):
        raise ConnectionError("Packet payload missing or corrupted.")

    # Retrieve the trusted signature for this device
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not expected_sig:
        # Unknown device; treat as untrusted
        return None

    # Perform a timing‑safe comparison of the signatures
    if not hmac.compare_digest(signature, expected_sig):
        return None

    # Signature verified; return the data payload
    return data