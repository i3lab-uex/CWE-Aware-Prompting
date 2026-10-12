import hmac
from typing import Dict, Optional

# Global mapping from device ID to its expected cryptographic signature.
# In a real deployment this would be stored securely, e.g. in a
# secrets manager or HSM.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (device_id : expected_signature)
    "device-001": "a3f4c2b9d6e7f8g1h2i3j4k5l6m7n8o9p0q1r2s3t4u5v6w7x8y9z0",
    "device-002": "b1c2d3e4f5g6h7i8j9k0l1m2n3o4p5q6r7s8t9u0v1w2x3y4z5a6b7c8d9e0f1",
    # Add more devices as needed
}


def process_packet_data(
    id_device: str, packet_signature: str, packet_data: Dict
) -> Optional[Dict]:
    """
    Validate the cryptographic signature of a data packet from an IoT device
    and return the packet payload if the signature is correct.

    Parameters
    ----------
    id_device : str
        Unique identifier of the IoT device sending the packet.
    packet_signature : str
        The cryptographic signature provided with the packet (hex string).
    packet_data : dict
        Payload of the packet.

    Returns
    -------
    dict or None
        The original `packet_data` if the signature is valid, otherwise None.

    Raises
    ------
    ConnectionError
        If the device ID is not recognized or there was an issue receiving data.
    """
    # Ensure we have a signature to validate against
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(id_device)
    if expected_signature is None:
        # Unknown device – treat as a connection/authorization error
        raise ConnectionError(f"Unrecognized device ID: {id_device}")

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(packet_signature, expected_signature):
        # Signature mismatch – data cannot be trusted
        return None

    # At this point the packet is authenticated; return its content
    return packet_data