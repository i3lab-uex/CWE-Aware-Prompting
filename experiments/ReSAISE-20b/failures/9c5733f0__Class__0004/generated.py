#!/usr/bin/env python3
"""
Module providing a secure packet authentication routine for IoT devices.
"""

import hmac
import hashlib
from typing import Dict, Optional

# Example trusted signatures mapping.
# In production this should be loaded from a secure store or HSM.
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # device_id : hex_encoded_hmac_sha256_signature
    "device_001": "3a7bd3e2360a4d9f5c1b2e6f8a7e3c5b1d4e9f0a2b3c6d8e9f01234567890ab",
    # Add more device signatures as needed.
}


def process_packet_data(
    id_device: str,
    packet_signature: str,
    packet_data: Dict
) -> Optional[Dict]:
    """
    Authenticate and process a data packet from an IoT device.

    Parameters
    ----------
    id_device : str
        Unique identifier of the sending IoT device.
    packet_signature : str
        Hex‑encoded cryptographic signature attached to the packet.
    packet_data : dict
        The actual content of the packet.

    Returns
    -------
    dict or None
        The original `packet_data` if the signature is valid; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the device is unknown or if there was an issue retrieving its trusted signature.
    """
    # Ensure the device ID is known
    if id_device not in TRUSTED_DEVICE_SIGNATURES:
        raise ConnectionError(f"Unknown device ID: {id_device}")

    # Retrieve the expected signature for this device
    try:
        expected_sig_hex = TRUSTED_DEVICE_SIGNATURES[id_device]
    except KeyError as exc:  # defensive, should not happen
        raise ConnectionError(f"Failed to retrieve signature for device {id_device}") from exc

    # Validate that the provided signature is a valid hex string
    try:
        packet_sig_bytes = bytes.fromhex(packet_signature)
        expected_sig_bytes = bytes.fromhex(expected_sig_hex)
    except ValueError as exc:
        raise ConnectionError("Invalid signature format") from exc

    # Compute the HMAC over the serialized packet data using a secure hash function
    # Here we assume that the packet_data is serialised deterministically.
    # For real deployments, use a robust serialization format (e.g., CBOR or JSON with sorted keys).
    serialized = str(packet_data).encode("utf-8")
    computed_hmac = hmac.new(
        key=expected_sig_bytes,
        msg=serialized,
        digestmod=hashlib.sha256
    ).digest()

    # Constant‑time comparison to mitigate timing attacks (CWE-345)
    if hmac.compare_digest(computed_hmac, packet_sig_bytes):
        return packet_data

    # Signature mismatch; reject the data
    return None


# Example usage (for testing only, remove in production)
if __name__ == "__main__":
    sample_id = "device_001"
    sample_data = {"temperature": 22.5, "humidity": 45}
    # Simulate a correct signature
    key = bytes.fromhex(TRUSTED_DEVICE_SIGNATURES[sample_id])
    serialized = str(sample_data).encode("utf-8")
    correct_sig = hmac.new(key, serialized, hashlib.sha256).hexdigest()

    result = process_packet_data(sample_id, correct_sig, sample_data)
    print("Result:", result)  # Should output the packet data