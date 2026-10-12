#!/usr/bin/env python3
"""
Utility for validating IoT device data packets.

The module defines a single public function, `verify_iot_signature`, which
ensures that a data packet received from an IoT device carries a valid
cryptographic signature before it is processed further.
"""

from __future__ import annotations

import hashlib
from typing import Any, Dict, Optional

# --------------------------------------------------------------------------- #
# Global dictionary mapping IoT device IDs to the expected cryptographic
# signature. In a real-world scenario, this would be populated from a secure
# source such as a database or a secrets manager.
# --------------------------------------------------------------------------- #
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries (signature values are SHA-256 hex digests)
    "device_001": "5d41402abc4b2a76b9719d911017c592",
    "device_002": "7d793037a0760186574b0282f2f435e7",
    # Add more device IDs and their corresponding signatures here.
}


def _compute_signature(data: Dict[str, Any]) -> str:
    """
    Compute a deterministic SHA-256 signature for the given packet data.

    The function serialises the dictionary in a stable order to ensure
    consistent signatures across different executions.

    Parameters:
        data: The packet content as a dictionary.

    Returns:
        A hexadecimal string representing the SHA-256 hash.
    """
    # Convert dictionary to a sorted tuple of items to guarantee order
    serialised = str(sorted(data.items())).encode("utf-8")
    return hashlib.sha256(serialised).hexdigest()


def verify_iot_signature(
    iot_id: str, crypto_signature: str, packet_info: Optional[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """
    Validate the cryptographic signature of an IoT data packet.

    The function performs the following steps:
        1. Checks that a connection to the IoT device could be established
           (simulated by ensuring `packet_info` is not None).
        2. Verifies that the device ID exists in the trusted registry.
        3. Computes the expected signature for the packet content and compares
           it with the supplied `crypto_signature`.
        4. Returns the packet data if the signature matches, otherwise returns
           ``None``.

    Parameters:
        iot_id (str): Unique identifier for the IoT device.
        crypto_signature (str): The cryptographic signature attached to
                                the data packet. Expected to be a hex string.
        packet_info (dict): The actual content of the data packet.

    Returns:
        dict | None: The packet dictionary if signature is valid,
                     otherwise ``None``.

    Raises:
        ConnectionError: If the packet data could not be received
                         (i.e., ``packet_info`` is ``None``).
    """
    # 1. Simulate a connection check
    if packet_info is None:
        raise ConnectionError("Failed to receive data from IoT device.")

    # 2. Verify that the device is trusted
    expected_signature = TRUSTED_DEVICE_SIGNATURES.get(iot_id)
    if expected_signature is None:
        # Unknown device – treat as a security failure
        return None

    # 3. Compute the signature of the packet content
    computed_signature = _compute_signature(packet_info)

    # 4. Compare signatures securely using constant-time comparison
    if hashlib.compare_digest(computed_signature, crypto_signature):
        return packet_info

    # Signature mismatch – data cannot be trusted
    return None


# --------------------------------------------------------------------------- #
# Example usage (for demonstration purposes only – remove or guard with
# `if __name__ == "__main__":` in production code).
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    sample_packet = {"temperature": 22.5, "humidity": 45}
    iot_id_sample = "device_001"
    # Compute a matching signature for the sample packet
    correct_sig = _compute_signature(sample_packet)

    result = verify_iot_signature(iot_id_sample, correct_sig, sample_packet)
    print("Verification result:", result)