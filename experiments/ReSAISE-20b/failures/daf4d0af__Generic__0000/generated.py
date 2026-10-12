import logging
from typing import Dict, Any

# Global dictionary mapping device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "1234567890abcdef",
    # Add more device signatures as needed
}

# Configure a basic logger for debugging purposes.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_data_packet(device_id: str, signature: str, data: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Process a data packet received from an IoT device after verifying its cryptographic signature.

    Parameters
    ----------
    device_id : str
        The identification number of the IoT device that sent the data.
    signature : str
        The cryptographic signature accompanying the packet.
    data : dict
        The payload of the packet that needs to be processed.

    Returns
    -------
    dict | None
        The data dictionary if the signature is valid; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the packet is not received properly (e.g., missing or invalid arguments).
    """
    # Basic validation of input types.
    if not isinstance(device_id, str):
        raise ConnectionError("Invalid device ID: must be a string.")
    if not isinstance(signature, str):
        raise ConnectionError("Invalid signature: must be a string.")
    if not isinstance(data, dict):
        raise ConnectionError("Invalid data payload: must be a dictionary.")

    # Retrieve the trusted signature for the device.
    trusted_signature = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if trusted_signature is None:
        logger.warning(f"Unknown device ID: {device_id}")
        return None

    # Verify the signature.
    if signature != trusted_signature:
        logger.warning(f"Signature mismatch for device {device_id}.")
        return None

    # If all checks pass, the data is considered trustworthy.
    logger.info(f"Data packet from device {device_id} verified successfully.")
    return data