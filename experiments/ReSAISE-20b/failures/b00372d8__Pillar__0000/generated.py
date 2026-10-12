#!/usr/bin/env python3
"""
IoT packet processor.

The module validates the cryptographic signature supplied with each
packet against a trusted list of signatures.  It uses constant‑time
comparison to mitigate timing attacks (CWE‑693).
"""

import hmac
import hashlib
from typing import Dict, Optional

# Global mapping of device_id -> expected HMAC signature (hex string)
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries – replace with real values
    "device_001": "d4f2a1b3c9e7f6a8b5c0d2e4f1a3b6c9d7e8f9a0b1c2d3e4f5a6b7c8d9e0f123",
    "device_002": "a1b2c3d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef0",
    # ...
}


def process_iot_packet(
    device_id: str,
    crypt_sig: str,
    pkt_data: Dict[str, any],
) -> Optional[Dict[str, any]]:
    """
    Validate and process a packet from an IoT device.

    Parameters
    ----------
    device_id : str
        Unique identifier of the sending IoT device.
    crypt_sig : str
        Cryptographic signature provided with the packet (hex string).
    pkt_data : dict
        Payload of the packet to be processed.

    Returns
    -------
    dict or None
        Processed data if signature is valid, otherwise None.

    Raises
    ------
    ConnectionError
        If the packet cannot be received (e.g., pkt_data is None or empty).
    """
    # Basic sanity check – a missing payload indicates a transmission error
    if pkt_data is None or not isinstance(pkt_data, dict):
        raise ConnectionError("Packet data could not be received")

    # Retrieve the expected signature for this device
    expected_sig = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if expected_sig is None:
        # Unknown device – treat as a potential attack
        return None

    # Normalize signatures to lowercase hex for comparison
    crypt_sig = crypt_sig.lower()
    expected_sig = expected_sig.lower()

    # Use constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(crypt_sig, expected_sig):
        # Signature mismatch – reject packet
        return None

    # At this point the signature is verified; process the payload.
    # For demonstration we simply return a copy of pkt_data with an added
    # timestamp and device ID.  Replace this with real business logic.
    processed = dict(pkt_data)  # shallow copy
    processed.update(
        {
            "device_id": device_id,
            "verified_at": int(hashlib.sha256().hexdigest(), 16) % (10**10),  # dummy timestamp
        }
    )
    return processed


# Example usage (commented out – remove if running in production)
if __name__ == "__main__":
    sample_packet = {"temperature": 22.5, "humidity": 45}
    try:
        result = process_iot_packet(
            device_id="device_001",
            crypt_sig=TRUSTED_DEVICE_SIGNATURES["device_001"],
            pkt_data=sample_packet,
        )
        print("Processed packet:", result)
    except ConnectionError as e:
        print(f"Connection error: {e}")