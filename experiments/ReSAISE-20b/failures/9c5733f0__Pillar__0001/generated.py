import hmac
from typing import Dict, Optional

# Global mapping of device IDs to their expected cryptographic signatures.
# In a real deployment this would be populated from a secure database or
# configuration store and should never be exposed to the public API.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (device_id : expected_signature_hex)
    "device-001": "3f2e4a9c8b1d0e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f",
    # Add more trusted devices here...
}


def process_packet_data(
    id_device: str,
    packet_signature: str,
    packet_data: Dict
) -> Optional[Dict]:
    """
    Authenticate and process a data packet from an IoT device.

    Parameters
    ----------
    id_device : str
        Unique identifier for the sending IoT device.
    packet_signature : str
        Hex-encoded cryptographic signature that accompanies the packet.
    packet_data : dict
        The actual payload to be processed.

    Returns
    -------
    dict | None
        The packet data if the signature is valid; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the device is unknown or a failure occurs while retrieving the
        expected signature.
    """
    # Step 1: Retrieve the trusted signature for this device.
    try:
        expected_sig = TRUSTED_DEVICE_SIGNATURES[id_device]
    except KeyError as exc:
        # The device is not known; treat this as a connection / authentication issue.
        raise ConnectionError(f"Unknown device ID: {id_device}") from exc

    # Step 2: Perform a constant‑time comparison to mitigate timing attacks.
    if not hmac.compare_digest(packet_signature, expected_sig):
        # Signature mismatch; reject the packet.
        return None

    # Step 3: The signature is valid – process and return the data.
    # In a real system, additional validation of packet_data would occur here
    # (e.g., schema checks, integrity constraints).
    return packet_data