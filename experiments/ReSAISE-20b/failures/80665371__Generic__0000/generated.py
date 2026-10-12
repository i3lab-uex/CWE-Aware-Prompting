import hmac
from typing import Dict, Optional

# Global dictionary mapping device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; replace with actual device IDs and signatures.
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "0j9i8h7g6f5e4d3c2b1a",
    # Add more devices as needed.
}


def process_data_packet(dev_id: str, sign: str, payload: Dict) -> Optional[Dict]:
    """
    Validate the cryptographic signature of a data packet from an IoT device
    and return the payload if the signature is verified.

    Parameters
    ----------
    dev_id : str
        The unique identifier of the IoT device that sent the packet.
    sign : str
        The cryptographic signature attached to the packet.
    payload : dict
        The actual data or payload to be processed.

    Returns
    -------
    Optional[dict]
        The original payload if the signature is verified, otherwise None.

    Raises
    ------
    ConnectionError
        If there are any issues receiving a data packet from the device.
    """
    # Basic sanity checks
    if not isinstance(dev_id, str) or not dev_id:
        raise ConnectionError("Missing or invalid device ID.")
    if not isinstance(sign, str) or not sign:
        raise ConnectionError("Missing or invalid signature.")
    if payload is None or not isinstance(payload, dict):
        raise ConnectionError("Missing or invalid payload.")

    # Retrieve the trusted signature for this device
    trusted_sig = TRUSTED_DEVICE_SIGNATURES.get(dev_id)
    if not trusted_sig:
        # Device is unknown – treat as a connection error
        raise ConnectionError(f"Untrusted device ID: {dev_id}")

    # Verify the signature.
    # In a real-world scenario, this would involve cryptographic checks (e.g., HMAC,
    # RSA verification, etc.). Here we perform a constant-time comparison to avoid
    # timing attacks.
    if not hmac.compare_digest(sign, trusted_sig):
        # Signature mismatch – do not trust the payload.
        return None

    # If we reach this point, the signature is verified.
    return payload