#!/usr/bin/env python3
"""
process_packet module

This module implements the `process_packet` function which authenticates and processes
data packets sent by IoT devices. The function uses HMAC‑SHA256 signatures to verify the
integrity and authenticity of each packet.

Security notes:
- The function uses `hmac.compare_digest` for constant‑time comparison to mitigate
  timing attacks (CWE-693).
- The signature is computed over a JSON canonical representation of the data packet
  to avoid ambiguities in serialization.
- Device secrets are stored in the global `TRUSTED_DEVICE_SIGNATURES` dictionary.
"""

import json
import hmac
import hashlib
from typing import Dict, Optional

# Global dictionary mapping device IDs to their secret keys (hex strings)
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (replace with real secrets)
    "device-001": "a1b2c3d4e5f60718293a4b5c6d7e8f90",
    "device-002": "1a2b3c4d5e6f708192a3b4c5d6e7f809",
    # Add more device secrets as needed
}


def _canonicalize(data: Dict) -> str:
    """
    Convert a dictionary to a canonical JSON string with sorted keys.
    This ensures deterministic serialization for signature computation.
    """
    return json.dumps(data, separators=(",", ":"), sort_keys=True)


def _compute_hmac(secret_hex: str, message: str) -> bytes:
    """
    Compute HMAC‑SHA256 of the given message using a secret key.

    Parameters:
        secret_hex (str): Hexadecimal representation of the secret key.
        message (str): The message to sign.

    Returns:
        bytes: The raw HMAC digest.
    """
    secret = bytes.fromhex(secret_hex)
    return hmac.new(secret, message.encode("utf-8"), hashlib.sha256).digest()


def process_packet(device_id: str, packet_signature: str, data_packet: Dict) -> Optional[Dict]:
    """
    Validate the cryptographic signature of a data packet and return the processed data.

    Parameters:
        device_id (str): Unique identifier of the IoT device.
        packet_signature (str): Hexadecimal signature sent with the packet.
        data_packet (dict): The content of the data packet.

    Returns:
        dict: The processed data if signature validation passes.
        None: If the signature is invalid.

    Raises:
        ConnectionError: If the device_id is unknown or packet cannot be received.
    """
    # 1. Ensure we have a trusted secret for the device
    if device_id not in TRUSTED_DEVICE_SIGNATURES:
        raise ConnectionError(f"Untrusted device: {device_id}")

    secret_hex = TRUSTED_DEVICE_SIGNATURES[device_id]

    # 2. Canonicalize the packet data
    try:
        canonical_data = _canonicalize(data_packet)
    except (TypeError, ValueError) as exc:
        raise ConnectionError(f"Invalid data packet format: {exc}") from exc

    # 3. Compute expected HMAC
    try:
        expected_hmac = _compute_hmac(secret_hex, canonical_data)
    except Exception as exc:
        raise ConnectionError(f"Failed to compute HMAC: {exc}") from exc

    # 4. Convert received signature to bytes
    try:
        received_hmac = bytes.fromhex(packet_signature)
    except ValueError as exc:
        raise ConnectionError(f"Malformed signature: {exc}") from exc

    # 5. Constant‑time comparison
    if not hmac.compare_digest(expected_hmac, received_hmac):
        # Signature mismatch: do not process packet
        return None

    # 6. Process the data (placeholder for real logic)
    processed_data = {
        "device_id": device_id,
        "payload": data_packet,  # In a real scenario, transform or validate the payload
    }

    return processed_data