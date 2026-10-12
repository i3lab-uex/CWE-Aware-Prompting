#!/usr/bin/env python3
"""
IoT packet authentication module.

This module implements the `process_packet_data` function, which verifies
the cryptographic signature of a packet received from an IoT device before
processing its content.  The verification is performed using a timing‑safe
comparison to mitigate side‑channel attacks (CWE‑693).

The module assumes the existence of a global dictionary
`TRUSTED_DEVICE_SIGNATURES` that maps each device ID to its shared secret.
"""

from __future__ import annotations

import hashlib
import hmac
from typing import Dict, Any, Optional

# --------------------------------------------------------------------------- #
# Global registry of trusted device secrets
# --------------------------------------------------------------------------- #

# Example structure:
# TRUSTED_DEVICE_SIGNATURES = {
#     "device_123": b"super_secret_key_for_device_123",
#     ...
# }
TRUSTED_DEVICE_SIGNATURES: Dict[str, bytes] = {}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _canonicalize_payload(payload: Dict[str, Any]) -> bytes:
    """
    Convert a payload dictionary into a deterministic byte representation
    suitable for hashing.  The keys are sorted alphabetically to ensure
    consistent ordering across different callers.

    Parameters:
        payload: The packet data dictionary.

    Returns:
        A UTF‑8 encoded byte string representing the canonical payload.
    """
    # Sort keys to ensure deterministic ordering
    items = sorted(payload.items())
    # Build a string representation: key1=value1;key2=value2;...
    parts = [f"{k}={v}" for k, v in items]
    canonical_str = ";".join(parts)
    return canonical_str.encode("utf-8")

def _compute_hmac(secret: bytes, message: bytes) -> str:
    """
    Compute a SHA‑256 HMAC of the given message using the provided secret key.

    Parameters:
        secret: The shared secret key (bytes).
        message: The canonical payload bytes.

    Returns:
        A hexadecimal string representation of the HMAC.
    """
    mac = hmac.new(secret, message, hashlib.sha256)
    return mac.hexdigest()

# --------------------------------------------------------------------------- #
# Main API
# --------------------------------------------------------------------------- #

def process_packet_data(
    id_device: str,
    packet_signature: str,
    packet_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Authenticate and process a packet from an IoT device.

    The function verifies that the provided `packet_signature` matches
    a freshly computed HMAC over the canonical representation of
    `packet_data`, using the device's shared secret stored in
    `TRUSTED_DEVICE_SIGNATURES`.  If the signature is valid, the original
    packet data dictionary is returned; otherwise, ``None`` is returned.

    A :class:`ConnectionError` is raised if packet data could not be
    received (e.g., the payload is ``None`` or empty), reflecting a
    communication issue with the device.

    Parameters:
        id_device: The unique identifier for the IoT device sending the data.
        packet_signature: The cryptographic signature attached to the packet.
        packet_data: The actual content of the packet (must be a dict).

    Returns:
        The original `packet_data` dictionary if authentication succeeds,
        otherwise ``None``.

    Raises:
        ConnectionError: If `packet_data` is missing or cannot be processed.
    """
    # Validate input types
    if not isinstance(id_device, str):
        raise TypeError("id_device must be a string")
    if not isinstance(packet_signature, str):
        raise TypeError("packet_signature must be a string")
    if not isinstance(packet_data, dict):
        raise ConnectionError("Failed to receive valid packet data from device")

    # Retrieve the shared secret for the device
    secret = TRUSTED_DEVICE_SIGNATURES.get(id_device)
    if secret is None:
        # Unknown device: treat as authentication failure
        return None

    try:
        # Canonicalize payload and compute HMAC
        canonical = _canonicalize_payload(packet_data)
        expected_signature = _compute_hmac(secret, canonical)

        # Timing‑safe comparison to mitigate side‑channel attacks
        if not hmac.compare_digest(expected_signature, packet_signature):
            return None

    except Exception as exc:
        # Any unexpected error during verification is treated as a failure
        # but not as a connection issue.
        raise RuntimeError(f"Authentication error: {exc}") from exc

    # Signature verified – return the original data
    return packet_data