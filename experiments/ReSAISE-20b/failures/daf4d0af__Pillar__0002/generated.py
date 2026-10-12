import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their trusted cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with real values in production.
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef1234",
}

def handle_data_packet(device_id: str, signature: str, data: Dict) -> Optional[Dict]:
    """
    Process a data packet from an IoT device after verifying its cryptographic signature.

    Args:
        device_id (str): The identification number of the IoT device that sent the data.
        signature (str): The cryptographic signature accompanying the packet.
        data (dict): The payload of the packet that needs to be processed.

    Returns:
        dict: The original data dictionary if the signature is valid.
        None: If the signature does not match the trusted value.

    Raises:
        ConnectionError: If the packet is malformed or any required field is missing.
    """
    # Validate input types and presence of required fields
    if not isinstance(device_id, str) or not device_id:
        raise ConnectionError("Missing or invalid device identifier.")
    if not isinstance(signature, str) or not signature:
        raise ConnectionError("Missing or invalid signature.")
    if not isinstance(data, dict):
        raise ConnectionError("Payload must be a dictionary.")

    # Retrieve the trusted signature for this device
    trusted_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not trusted_sig:
        # Unknown device – treat as a potential security threat
        raise ConnectionError(f"Unrecognized device ID: {device_id}")

    # Constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(signature, trusted_sig):
        # Signature mismatch – reject the packet
        return None

    # At this point, the signature is verified; safely return the data.
    return data