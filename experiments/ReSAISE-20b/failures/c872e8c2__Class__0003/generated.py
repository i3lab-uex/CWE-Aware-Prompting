import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their trusted cryptographic signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with real values in production
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "0123456789abcdef1234",
}

def manage_data_packet(
    io_device_id: str,
    crypto_signature: str,
    packet_data: Dict
) -> Optional[Dict]:
    """
    Validate the cryptographic signature of an incoming IoT data packet
    and return the payload if the signature is trusted.

    Parameters:
        io_device_id (str): Unique identifier of the sending IoT device.
        crypto_signature (str): Signature attached to the packet.
        packet_data (dict): The actual data payload.

    Returns:
        dict: The packet data if the signature is verified.
        None: If the signature does not match the trusted value.

    Raises:
        ConnectionError: If an error occurs while receiving or accessing packet data.
    """
    try:
        # Retrieve the trusted signature for this device
        trusted_sig = TRUSTED_DEVICE_SIGNATURES[io_device_id]
    except KeyError as exc:
        # Device ID unknown – treat this as a communication error
        raise ConnectionError(
            f"Unknown device ID '{io_device_id}'. Unable to verify signature."
        ) from exc

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(crypto_signature, trusted_sig):
        # Signature mismatch – reject the packet
        return None

    # At this point, signature is verified; safely return payload
    return packet_data