import json
import hmac
import hashlib

# Global dictionary mapping device IDs to their shared secret keys (hex strings)
TRUSTED_DEVICE_SIGNATURES = {
    # Example entries – replace with actual device keys
    "device_001": "a1b2c3d4e5f60718293a4b5c6d7e8f90",
    "device_002": "00112233445566778899aabbccddeeff",
}

def _compute_hmac(secret_key: bytes, payload: dict) -> str:
    """
    Compute the HMAC‑SHA256 over the canonical JSON representation of *payload*.
    The payload is serialized with sorted keys to guarantee deterministic ordering.
    """
    json_bytes = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hmac.new(secret_key, json_bytes, hashlib.sha256).hexdigest()

def verify_data_packet(device: str, sig: str, payload: dict) -> dict | None:
    """
    Validate a data packet from an IoT device.

    Parameters
    ----------
    device : str
        Unique identifier of the sending device.
    sig : str
        Hexadecimal cryptographic signature attached to the packet.
    payload : dict
        The actual data to be processed.

    Returns
    -------
    dict | None
        The payload dictionary if the signature is verified, otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the device is unknown or if there are issues retrieving its secret key.
    """
    # Retrieve the shared secret for this device
    try:
        secret_hex = TRUSTED_DEVICE_SIGNATURES[device]
    except KeyError as exc:
        # Unknown device – treat this as a connectivity / authentication failure
        raise ConnectionError(f"Unknown or untrusted device: {device}") from exc

    # Convert the hex key to bytes
    secret_key = bytes.fromhex(secret_hex)

    try:
        expected_sig = _compute_hmac(secret_key, payload)
    except Exception as exc:  # pragma: no cover
        # Any error during HMAC computation is treated as a communication issue
        raise ConnectionError("Failed to compute signature for verification") from exc

    # Constant‑time comparison to mitigate timing attacks
    if hmac.compare_digest(expected_sig, sig):
        return payload
    return None