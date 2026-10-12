import hmac
import hashlib

# Global dictionary mapping device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES = {
    # Example entries (replace with real values)
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef1234",
}

def handle_data_packet(device_id: str, signature: str, data: dict):
    """
    Process an IoT device data packet after verifying its cryptographic signature.

    Parameters
    ----------
    device_id : str
        Identification number of the IoT device that sent the data.
    signature : str
        Cryptographic signature accompanying the packet.
    data : dict
        Payload of the packet that needs to be processed.

    Returns
    -------
    dict or None
        The original data dictionary if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the packet is not received properly (e.g., missing fields or empty payload).
    """
    # Basic validation of inputs
    if not device_id or not signature or data is None:
        raise ConnectionError("Data packet received improperly: missing fields.")

    # Retrieve the trusted signature for this device
    trusted_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if not trusted_sig:
        # Device unknown or untrusted
        return None

    # Use constant‑time comparison to prevent timing attacks
    if not hmac.compare_digest(signature, trusted_sig):
        # Signature mismatch
        return None

    # All checks passed; return the data payload
    return data