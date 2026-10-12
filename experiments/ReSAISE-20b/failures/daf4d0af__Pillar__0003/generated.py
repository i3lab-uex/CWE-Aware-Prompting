import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their trusted cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with actual device IDs and signatures.
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "0123456789abcdef1234",
}

def handle_data_packet(device_id: str, signature: str, data: Dict) -> Optional[Dict]:
    """
    Process an incoming IoT data packet after verifying its cryptographic signature.

    Parameters
    ----------
    device_id : str
        The identification number of the IoT device that sent the data.
    signature : str
        The cryptographic signature that accompanies the packet.
    data : dict
        The payload of the packet to be processed.

    Returns
    -------
    dict | None
        The data dictionary if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the packet is not received properly (e.g., missing arguments or invalid data type).
    """
    # Validate that all required inputs are present and of the expected type.
    if not isinstance(device_id, str) or not device_id:
        raise ConnectionError("Invalid or missing device ID.")
    if not isinstance(signature, str) or not signature:
        raise ConnectionError("Invalid or missing signature.")
    if not isinstance(data, dict):
        raise ConnectionError("Payload must be a dictionary.")

    # Retrieve the trusted signature for this device, if any.
    trusted_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not trusted_sig:
        # Device is unknown or untrusted – reject the packet.
        return None

    # Perform a constant‑time comparison to mitigate timing attacks.
    if not hmac.compare_digest(signature, trusted_sig):
        # Signature does not match – reject the packet.
        return None

    # Signature is valid; return the payload as-is (or perform any additional
    # processing required by the application here).
    return data