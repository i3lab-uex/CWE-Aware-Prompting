import hmac
from typing import Dict, Any

# Global mapping of device IDs to the expected cryptographic signature.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; in production these would be securely stored.
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef",
}

def verify_iot_signature(
    iot_id: str,
    crypto_signature: str,
    packet_info: Dict[str, Any]
) -> Dict[str, Any] | None:
    """
    Validate the cryptographic signature of an IoT data packet and return
    the packet content if valid.

    Parameters
    ----------
    iot_id : str
        Unique identifier for the IoT device.
    crypto_signature : str
        Signature attached to the data packet.
    packet_info : dict
        The actual content of the packet.

    Returns
    -------
    dict | None
        The packet content if signature is valid, otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the packet is missing required fields or cannot be retrieved.
    """
    # 1. Ensure we have the packet data; if not, raise an error.
    if not isinstance(packet_info, dict) or "data" not in packet_info:
        raise ConnectionError("Failed to receive complete data from IoT device")

    # 2. Retrieve the expected signature for this device.
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(iot_id)
    if expected_signature is None:
        # Unknown device – treat as a failure to avoid spoofing.
        return None

    # 3. Use constant‑time comparison to guard against timing attacks
    # (CWE-347: Improper Verification of Cryptographic Signature).
    if not hmac.compare_digest(crypto_signature, expected_signature):
        # Signature mismatch – reject the packet.
        return None

    # 4. If we reach here, signature is valid; return the packet content.
    return packet_info