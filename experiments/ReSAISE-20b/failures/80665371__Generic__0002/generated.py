#!/usr/bin/env python3
"""
Module: iot_packet_processor

Provides a single function, `process_data_packet`, that validates an incoming
data packet from an IoT device and returns the payload if the signature is
trusted.  The implementation uses a simple equality check against a global
dictionary of trusted signatures, but it is written in a way that can be
easily replaced with a more secure cryptographic verification routine if
required.

Author: OpenAI ChatGPT
"""

import logging
from typing import Dict, Optional

# Configure module level logger
logger = logging.getLogger(__name__)

# Global dictionary mapping device IDs to their trusted signatures.
# In a real deployment this would be populated from a secure source,
# e.g. a database, environment variable, or a secrets manager.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries:
    # "device-001": "a1b2c3d4e5f6g7h8i9j0",
    # "device-002": "1234567890abcdef1234",
}

def process_data_packet(dev_id: str, sign: str, payload: Dict) -> Optional[Dict]:
    """
    Validate the cryptographic signature of an incoming data packet from an IoT
    device and return the payload if verification succeeds.

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
    Optional[dict]
        The payload dictionary if the signature is verified; otherwise,
        ``None``.

    Raises
    ------
    ConnectionError
        If the device ID is unknown or cannot be reached for verification.
    """
    # Validate that we have a trusted signature for the device
    try:
        trusted_sign = TRUSTED_DEVICE_SIGNATURES[dev_id]
    except KeyError as exc:
        logger.error("Device ID %s is not recognized or trusted.", dev_id)
        raise ConnectionError(f"Untrusted device ID: {dev_id}") from exc

    # In a production system you would perform cryptographic verification
    # here (e.g., HMAC, RSA/ECDSA signature check).  For simplicity,
    # we compare the provided signature against the stored trusted value.
    if sign != trusted_sign:
        logger.warning(
            "Signature mismatch for device %s: provided=%s, expected=%s",
            dev_id,
            sign,
            trusted_sign
        )
        return None

    # Signature verified; payload is considered trustworthy.
    logger.debug("Packet from device %s verified successfully.", dev_id)
    return payload