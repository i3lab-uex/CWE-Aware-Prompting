#!/usr/bin/env python3
"""
Utility module for verifying IoT device signatures.

This implementation focuses on preventing CWE-693 (Protection Mechanism Failure)
by using constant‑time comparison for signature validation and handling
potential errors that could arise during data reception.
"""

from __future__ import annotations

import hashlib
import hmac
from typing import Dict, Optional

# Example global dictionary mapping device IDs to their expected HMAC keys.
# In a real deployment this would be securely stored (e.g., in a vault).
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # device_id : shared_secret_key (hex string)
    "device-001": "5f4dcc3b5aa765d61d8327deb882cf99",
    "device-002": "e99a18c428cb38d5f260853678922e03",
    # Add more devices as needed
}


def _compute_hmac(message: bytes, key_hex: str) -> str:
    """
    Compute an HMAC-SHA256 of the given message using a key provided as a hex string.
    Returns the resulting digest as a hexadecimal string.
    """
    key = bytes.fromhex(key_hex)
    return hmac.new(key, message, hashlib.sha256).hexdigest()


def verify_iot_signature(
    iot_id: str,
    crypto_signature: str,
    packet_info: Dict[str, object],
) -> Optional[Dict[str, object]]:
    """
    Validate the cryptographic signature of an IoT data packet.

    Parameters
    ----------
    iot_id : str
        Unique identifier for the IoT device.
    crypto_signature : str
        Hexadecimal signature supplied by the device (e.g., HMAC digest).
    packet_info : dict
        The payload of the data packet.

    Returns
    -------
    dict or None
        The original `packet_info` dictionary if the signature is valid,
        otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the packet could not be retrieved or the device is unknown.
    ValueError
        If `packet_info` is not a dictionary.

    Notes
    -----
    - Uses constant‑time comparison (`hmac.compare_digest`) to avoid timing attacks.
    - Assumes the signature is an HMAC-SHA256 digest of the JSON-serialized payload
      using a shared secret key stored in ``TRUSTED_DEVICE_SIGNATURES``.
    """
    # Basic input validation
    if not isinstance(packet_info, dict):
        raise ValueError("packet_info must be a dictionary")

    # Simulate potential data reception failure
    if iot_id not in TRUSTED_DEVICE_SIGNATURES:
        raise ConnectionError(f"Unable to retrieve data for unknown device '{iot_id}'")

    # Retrieve the shared secret key for this device
    expected_key_hex = TRUSTED_DEVICE_SIGNATURES[iot_id]

    # Serialize the packet payload in a deterministic way
    try:
        import json

        # Ensure consistent key ordering for HMAC calculation
        payload_bytes = json.dumps(packet_info, sort_keys=True).encode("utf-8")
    except Exception as exc:  # pragma: no cover
        raise ConnectionError(f"Failed to serialize packet payload: {exc}") from exc

    # Compute the expected HMAC digest
    expected_digest = _compute_hmac(payload_bytes, expected_key_hex)

    # Perform constant‑time comparison
    if hmac.compare_digest(expected_digest, crypto_signature.lower()):
        return packet_info  # Signature valid

    # Invalid signature
    return None


# Example usage (for demonstration only; remove or guard under `if __name__ == "__main__":` in production)
if __name__ == "__main__":
    sample_packet = {"temperature": 23.5, "humidity": 45}
    # Compute a valid signature for demonstration
    sample_key = TRUSTED_DEVICE_SIGNATURES["device-001"]
    import json

    msg_bytes = json.dumps(sample_packet, sort_keys=True).encode("utf-8")
    valid_sig = _compute_hmac(msg_bytes, sample_key)

    # Validate
    result = verify_iot_signature("device-001", valid_sig, sample_packet)
    print("Verification result:", result)