import json
import hmac
import hashlib
from typing import Dict, Optional

# Global dictionary mapping device IDs to their secret keys (or public keys if asymmetric)
TRUSTED_DEVICE_SIGNATURES: Dict[str, str] = {
    # Example entries; in production these would be securely stored
    "device-001": "my_secret_key_1",
    "device-002": "my_secret_key_2",
}


def _canonicalize_payload(data: Dict) -> bytes:
    """
    Convert the data dictionary to a canonical JSON representation.
    This ensures that the same logical payload always produces the same
    byte sequence for signature verification.

    Args:
        data: The data dictionary received from the device.

    Returns:
        A UTF‑8 encoded byte string of the canonical JSON.
    """
    # Sort keys to ensure deterministic ordering
    json_str = json.dumps(data, separators=(",", ":"), sort_keys=True)
    return json_str.encode("utf-8")


def _verify_hmac_signature(secret: str, payload_bytes: bytes, signature_hex: str) -> bool:
    """
    Verify an HMAC‑SHA256 signature.

    Args:
        secret: The shared secret key.
        payload_bytes: The canonicalized payload bytes.
        signature_hex: The hex string of the received signature.

    Returns:
        True if the signatures match, False otherwise.
    """
    try:
        # Compute HMAC of the payload
        computed_hmac = hmac.new(
            key=secret.encode("utf-8"),
            msg=payload_bytes,
            digestmod=hashlib.sha256
        ).hexdigest()
        # Use constant‑time comparison to avoid timing attacks
        return hmac.compare_digest(computed_hmac, signature_hex)
    except Exception:
        # Any error during verification is treated as a failure
        return False


def validate_device_packet(
    iot_device_id: str,
    iot_signature: str,
    iot_data: Dict
) -> Optional[Dict]:
    """
    Validate and process a data packet from an IoT device.

    The function performs the following steps:
        1. Checks that the packet was received (iot_data is not None).
        2. Retrieves the trusted secret for the device.
        3. Canonicalizes the payload and verifies the HMAC‑SHA256 signature.
        4. Returns the original data dictionary if validation succeeds,
           otherwise returns None.

    Args:
        iot_device_id: Unique identifier of the sending device.
        iot_signature: Hex‑encoded signature sent by the device.
        iot_data: The payload dictionary received.

    Returns:
        The processed data as a dictionary if the signature is valid,
        otherwise None.

    Raises:
        ConnectionError: If the packet cannot be received (iot_data is None).
    """
    # 1. Ensure we actually have data
    if iot_data is None:
        raise ConnectionError(f"Failed to receive packet from device {iot_device_id}")

    # 2. Get the trusted secret for this device
    secret = TRUSTED_DEVICE_SIGNATURES.get(iot_device_id)
    if not secret:
        # Unknown device; treat as a validation failure
        return None

    # 3. Canonicalize payload and verify signature
    payload_bytes = _canonicalize_payload(iot_data)
    if not _verify_hmac_signature(secret, payload_bytes, iot_signature):
        return None

    # 4. Validation succeeded; return the data as is
    return iot_data