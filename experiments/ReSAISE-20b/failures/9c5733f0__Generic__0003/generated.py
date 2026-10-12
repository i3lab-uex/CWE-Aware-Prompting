from __future__ import annotations

import logging
from typing import Dict, Optional

# Global mapping of device IDs to the expected cryptographic signature.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries – in a real system these would be securely stored.
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef",
}

def process_packet_data(
    id_device: str,
    packet_signature: str,
    packet_data: Optional[Dict],
) -> Optional[Dict]:
    """
    Validate a data packet from an IoT device and return the payload if
    authentication succeeds.

    Parameters
    ----------
    id_device : str
        Unique identifier of the sending device.
    packet_signature : str
        Cryptographic signature that accompanies the packet.
    packet_data : dict | None
        The actual payload of the packet.

    Returns
    -------
    dict | None
        The original packet data if signature verification passes;
        otherwise ``None``.

    Raises
    ------
    ConnectionError
        If packet_data is missing or the device cannot be found in the trusted list,
        indicating a failure to receive a proper packet from the IoT device.
    """
    # Basic sanity check – if we don't have data, treat it as a reception error.
    if packet_data is None:
        logging.error("No packet data received for device %s.", id_device)
        raise ConnectionError(f"Failed to receive data from device {id_device}")

    # Ensure the device is known and we have a stored signature to compare against.
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(id_device)
    if expected_sig is None:
        logging.warning("Unrecognized device ID: %s", id_device)
        raise ConnectionError(f"Unknown device {id_device}")

    # Verify the signature. In a real implementation this would involve cryptographic
    # checks (e.g., HMAC, RSA). Here we perform a simple equality check for
    # demonstration purposes.
    if packet_signature != expected_sig:
        logging.warning(
            "Signature mismatch for device %s: received=%s, expected=%s",
            id_device,
            packet_signature,
            expected_sig,
        )
        return None

    # Signature is valid – return the payload unchanged.
    logging.info("Packet from device %s authenticated successfully.", id_device)
    return packet_data