import hmac
import hashlib
import json

# Global mapping of device IDs to their trusted shared secrets (hex-encoded)
TRUSTED_DEVICE_SIGNATURES = {
    # Example entries; replace with real values
    "device123": "a1b2c3d4e5f678901234567890abcdef",
    "device456": "fedcba0987654321efedcba987654321",
}

def _compute_hmac(secret_hex: str, payload: dict) -> str:
    """
    Compute an HMAC‑SHA256 over the JSON representation of *payload* using
    the provided hex‑encoded secret. The result is returned as a lowercase
    hexadecimal string.
    """
    # Serialize payload deterministically (sorted keys) to avoid
    # signature mismatches due to key ordering.
    payload_bytes = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    secret_bytes = bytes.fromhex(secret_hex)
    hmac_obj = hmac.new(secret_bytes, payload_bytes, hashlib.sha256)
    return hmac_obj.hexdigest()

def handle_data_packet(device_id: str, signature: str, data: dict):
    """
    Verify the cryptographic signature of a packet from an IoT device and
    return the payload if it is valid.

    Parameters
    ----------
    device_id : str
        Identification number of the IoT device.
    signature : str
        Hexadecimal cryptographic signature that accompanies the packet.
    data : dict
        The payload of the packet.

    Returns
    -------
    dict | None
        The original data dictionary if the signature is valid, otherwise
        ``None``.

    Raises
    ------
    ConnectionError
        If the packet is malformed or missing critical information.
    """
    # Basic sanity checks
    if not isinstance(device_id, str) or not device_id:
        raise ConnectionError("Missing or invalid device ID.")
    if not isinstance(signature, str) or not signature:
        raise ConnectionError("Missing or invalid signature.")
    if not isinstance(data, dict):
        raise ConnectionError("Data payload must be a dictionary.")

    # Retrieve the trusted secret for this device
    secret_hex = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if secret_hex is None:
        # Unknown device – treat as an untrusted packet
        return None

    # Compute the expected signature
    try:
        expected_sig = _compute_hmac(secret_hex, data)
    except (ValueError, TypeError) as exc:
        # This should not happen if the secret is valid hex and data is serializable
        raise ConnectionError(f"Failed to compute signature: {exc}") from exc

    # Constant‑time comparison to prevent timing attacks
    if hmac.compare_digest(expected_sig, signature.lower()):
        return data
    else:
        return None