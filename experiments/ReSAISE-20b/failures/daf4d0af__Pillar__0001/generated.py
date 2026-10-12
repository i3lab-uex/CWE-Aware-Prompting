#!/usr/bin/env python3
"""
IoT data packet handler.

The function verifies the cryptographic signature of a received packet
against a trusted list before returning the payload.  It uses constant‑time
comparison to mitigate timing attacks (CWE‑693).

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import hmac
from typing import Dict, Any, Optional

# Global dictionary mapping device IDs to their trusted signatures.
# In a real system this would be populated from a secure source.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries:
    "device_001": "a1b2c3d4e5f6g7h8i9j0",
    "device_002": "deadbeefcafebabe1234",
}

def handle_data_packet(
    device_id: str,
    signature: str,
    data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Validate an IoT data packet and return the payload if trusted.

    Parameters
    ----------
    device_id : str
        Identification number of the sending IoT device.
    signature : str
        Cryptographic signature that accompanies the packet.
    data : dict
        The payload of the packet.

    Returns
    -------
    dict or None
        The original data dictionary if the signature is valid; otherwise,
        ``None``.  Raises :class:`ConnectionError` if the packet is not
        received properly.

    Raises
    ------
    ConnectionError
        If the packet data is missing or not a dictionary.
    """
    # Basic sanity check for the received packet
    if data is None or not isinstance(data, dict):
        raise ConnectionError("Data packet not received properly")

    # Retrieve the trusted signature for this device
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)

    # If the device is unknown or the signature does not match, reject
    if expected_sig is None:
        return None

    # Use constant‑time comparison to prevent timing attacks
    if not hmac.compare_digest(signature, expected_sig):
        return None

    # All checks passed; return the payload
    return data