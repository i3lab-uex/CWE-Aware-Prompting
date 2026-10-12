# process_data_packet.py

"""
Utility for validating and processing IoT data packets.
"""

from typing import Dict, Optional
import logging

# Configure a basic logger for debugging and audit purposes.
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

# Global dictionary mapping device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; replace with real device signatures.
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef",
}


def process_data_packet(dev_id: str, sign: str, payload: Dict) -> Optional[Dict]:
    """
    Validate a data packet from an IoT device and return the payload if verified.

    Parameters
    ----------
    dev_id : str
        Unique identifier of the IoT device that sent the packet.
    sign : str
        Cryptographic signature attached to the packet.
    payload : dict
        The actual data or payload to be processed.

    Returns
    -------
    dict | None
        The payload if the signature matches the trusted signature; otherwise None.

    Raises
    ------
    ConnectionError
        If the device ID is unknown or if there are issues receiving a packet.
    """
    # Ensure we have a trusted signature for this device
    if dev_id not in TRUSTED_DEVICE_SIGNATURES:
        logging.error("Unknown device ID: %s", dev_id)
        raise ConnectionError(f"Device '{dev_id}' is not trusted or unreachable.")

    # Retrieve the expected signature
    expected_sign = TRUSTED_DEVICE_SIGNATURES[dev_id]

    # Verify the signature. In a real implementation this would involve cryptographic
    # operations (e.g., HMAC, RSA). For demonstration we use a simple equality check.
    if sign != expected_sign:
        logging.warning(
            "Signature mismatch for device %s. Expected: %s, Received: %s",
            dev_id,
            expected_sign,
            sign,
        )
        return None

    # If verification passes, log success and return the payload.
    logging.info("Packet from device %s verified successfully.", dev_id)
    return payload