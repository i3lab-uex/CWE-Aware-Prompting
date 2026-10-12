#!/usr/bin/env python3
"""
IoT data packet validator.

This module defines a single public function, `manage_data_packet`, which
verifies the cryptographic signature of an incoming packet from an IoT device.
The function uses constant‑time comparison to avoid timing attacks
(CWE-347).  If the device is unknown a `ConnectionError` is raised,
otherwise the payload dictionary is returned on success or `None`
if the signature does not match.

The global mapping ``TRUSTED_DEVICE_SIGNATURES`` should be populated
elsewhere in the application with trusted signatures for each device.
"""

import hmac
from typing import Dict, Optional

# Global mapping of device ID -> trusted signature (hex encoded string)
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (replace with real values)
    "device-001": "a1b2c3d4e5f678901234567890abcdef",
    "device-002": "deadbeefcafebabe1234567890abcdef",
}


def manage_data_packet(
    io_device_id: str,
    crypto_signature: str,
    packet_data: Dict,
) -> Optional[Dict]:
    """
    Validate and process an incoming IoT data packet.

    Parameters
    ----------
    io_device_id : str
        Unique identifier of the device that sent the packet.
    crypto_signature : str
        Hex‑encoded cryptographic signature attached to the packet.
    packet_data : dict
        The actual payload to be processed.

    Returns
    -------
    dict or None
        The original packet data if the signature is verified,
        otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the device ID is unknown or there was an issue receiving the packet.
    """
    # Verify that we have a known device
    if io_device_id not in TRUSTED_DEVICE_SIGNATURES:
        raise ConnectionError(f"Unknown device ID: {io_device_id}")

    # Retrieve the expected signature for this device
    expected_sig = TRUSTED_DEVICE_SIGNATURES[io_device_id]

    # Ensure both signatures are in the same format (hex strings)
    try:
        crypto_sig_bytes = bytes.fromhex(crypto_signature.strip())
        expected_sig_bytes = bytes.fromhex(expected_sig.strip())
    except ValueError as exc:
        raise ConnectionError(
            "Signature format error; expected hex-encoded string."
        ) from exc

    # Constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(crypto_sig_bytes, expected_sig_bytes):
        # Signature mismatch – do not trust the data
        return None

    # Signature verified; safely return the payload
    return packet_data