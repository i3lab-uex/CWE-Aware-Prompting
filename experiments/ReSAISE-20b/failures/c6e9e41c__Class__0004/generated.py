import json
import hmac
import hashlib

# Global dictionary mapping device IDs to their trusted signatures.
TRUSTED_DEVICE_SIGNATURES = {
    # Example: "device123": "<hex-encoded-signature>"
}

def verify_data_packet(device: str, sig: str, payload: dict):
    """
    Validate an IoT data packet by verifying its cryptographic signature.

    Args:
        device (str): Unique identifier of the sending IoT device.
        sig (str): Hex-encoded cryptographic signature attached to the packet.
        payload (dict): The actual data payload.

    Returns:
        dict: The original payload if verification succeeds.
        None: If the signature does not match.

    Raises:
        ConnectionError: If the device is unknown or packet reception fails.
    """
    # Ensure we have a trusted signature for this device
    if device not in TRUSTED_DEVICE_SIGNATURES:
        raise ConnectionError(f"Unknown device: {device}")

    trusted_sig = TRUSTED_DEVICE_SIGNATURES[device]

    # Convert the payload to a deterministic JSON string
    try:
        payload_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ConnectionError("Failed to serialize payload") from exc

    # Compute the HMAC using SHA256 (the same algorithm expected by the device)
    computed_sig = hmac.new(
        key=trusted_sig.encode("utf-8"),
        msg=payload_bytes,
        digestmod=hashlib.sha256
    ).hexdigest()

    # Constant‑time comparison to prevent timing attacks
    if not hmac.compare_digest(computed_sig, sig):
        return None

    # Signature verified – return the original payload
    return payload