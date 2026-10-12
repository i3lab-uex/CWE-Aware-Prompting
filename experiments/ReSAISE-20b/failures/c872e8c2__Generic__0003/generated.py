# -*- coding: utf-8 -*-
"""
Utility module for processing IoT data packets with signature verification.
"""

import hashlib
from typing import Dict, Optional

# Global mapping of device IDs to their expected cryptographic signatures.
# In a real system this would be securely stored and managed, e.g. in
# a HSM or a dedicated secrets manager.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (device_id : expected_signature)
    "device-001": "a3f9c2e1d4b5c6f7e8a9b0c1d2e3f4a5",
    "device-002": "b7e6c5d4f3a2b1c0d9e8f7a6b5c4d3e2",
    # Add more devices as needed
}

def _compute_signature(payload: Dict) -> str:
    """
    Compute a deterministic signature for the given payload.
    For demonstration purposes we use SHA-256 over a sorted JSON string.
    In production, replace this with the actual signing algorithm used
    by your devices (e.g., ECDSA, RSA, HMAC).
    """
    import json
    # Ensure consistent ordering for hashing
    payload_str = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload_str.encode("utf-8")).hexdigest()

def manage_data_packet(
    io_device_id: str,
    crypto_signature: str,
    packet_data: Optional[Dict]
) -> Optional[Dict]:
    """
    Validate and process an incoming data packet from an IoT device.

    Parameters
    ----------
    io_device_id : str
        Unique identifier of the IoT device that sent the packet.
    crypto_signature : str
        Cryptographic signature attached to the packet.
    packet_data : dict | None
        The actual data or payload to be processed.

    Returns
    -------
    dict | None
        The packet data if the signature is verified successfully;
        otherwise, None.

    Raises
    ------
    ConnectionError
        If packet_data is missing or cannot be processed.
    """
    # Basic sanity checks
    if not io_device_id:
        raise ConnectionError("Missing device identifier.")
    if packet_data is None:
        raise ConnectionError(f"No data received from device {io_device_id}.")

    # Retrieve the expected signature for this device
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(io_device_id)
    if not expected_signature:
        # Unknown device – treat as untrusted
        return None

    # Compute the signature of the received payload
    try:
        computed_sig = _compute_signature(packet_data)
    except Exception as exc:
        # Any error in computing the signature is treated as a failure
        raise ConnectionError(
            f"Failed to compute signature for device {io_device_id}: {exc}"
        ) from exc

    # Verify the signature
    if computed_sig != crypto_signature:
        # Signature mismatch – data cannot be trusted
        return None

    # If we reach this point, the packet is verified and can be returned
    return packet_data