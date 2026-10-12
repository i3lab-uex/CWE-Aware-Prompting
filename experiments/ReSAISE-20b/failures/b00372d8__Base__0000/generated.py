#!/usr/bin/env python3
"""
IoT packet processor with secure cryptographic signature verification.

The module defines `process_iot_packet`, which validates an incoming packet
against a trusted signature before processing it.  It protects against
CWE‑347 (Improper Verification of Cryptographic Signature) by using a
constant‑time comparison and a secure HMAC implementation.

Author: OpenAI ChatGPT
"""

import hmac
import hashlib
from typing import Dict, Any

# Global mapping of device IDs to their secret HMAC keys.
TRUSTED_DEVICE_SIGNATURES: Dict[str, bytes] = {
    # Example entries – replace with real secrets in production.
    "device-001": b"supersecretkey123",
    "device-002": b"anothersecret456",
}

# The name of the hash algorithm used for HMAC.
HASH_ALGORITHM = hashlib.sha256


def _receive_packet(device_id: str) -> Dict[str, Any]:
    """
    Simulate receiving a packet from the device.

    In a real implementation this function would handle network I/O.
    For demonstration purposes, it simply raises an error to trigger
    the ConnectionError path if called.
    """
    raise NotImplementedError("Packet reception is not implemented in this demo.")


def _hmac_verify(message: bytes, key: bytes, signature: str) -> bool:
    """
    Verify that the provided hex signature matches the HMAC of `message`
    computed with `key` using a constant‑time comparison.

    :param message: The raw packet data as bytes.
    :param key:   Secret key for HMAC.
    :param signature: Hex‑encoded signature received from the device.
    :return: True if signatures match, False otherwise.
    """
    # Compute HMAC of the message
    hmac_obj = hmac.new(key, msg=message, digestmod=HASH_ALGORITHM)
    expected_sig = hmac_obj.hexdigest()

    # Constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(expected_sig, signature.lower())


def process_iot_packet(device_id: str, crypt_sig: str, pkt_data: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Validate the cryptographic signature of an IoT packet and process it.

    Parameters
    ----------
    device_id : str
        Unique identifier of the sending IoT device.
    crypt_sig : str
        Hex‑encoded cryptographic signature accompanying the packet.
    pkt_data : dict
        Payload of the data packet to be processed.

    Returns
    -------
    dict | None
        Processed packet data if the signature is valid; otherwise, `None`.

    Raises
    ------
    ConnectionError
        If the packet cannot be received successfully.
    """
    # 1. Ensure the device is trusted
    if device_id not in TRUSTED_DEVICE_SIGNATURES:
        # Unknown device – reject immediately
        return None

    key = TRUSTED_DEVICE_SIGNATURES[device_id]

    # 2. Receive packet (simulated). In a real system this would be I/O.
    try:
        _receive_packet(device_id)
    except NotImplementedError as exc:
        # In production, replace with actual network error handling
        raise ConnectionError(f"Failed to receive packet from {device_id}") from exc

    # 3. Serialize pkt_data into a deterministic byte string for HMAC.
    #    Use JSON with sorted keys to ensure consistent ordering.
    import json
    message_bytes = json.dumps(pkt_data, sort_keys=True, separators=(",", ":")).encode("utf-8")

    # 4. Verify the signature
    if not _hmac_verify(message_bytes, key, crypt_sig):
        # Signature mismatch – treat as tampered data
        return None

    # 5. Process the packet (placeholder – echo back with a status)
    processed = {
        "device_id": device_id,
        "status": "ok",
        "data": pkt_data,
    }
    return processed