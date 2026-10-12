import hmac
import hashlib

# Global dictionary mapping device IDs to their trusted HMAC secret keys (bytes).
TRUSTED_DEVICE_SIGNATURES = {
    # Example entries – replace with real secrets in production.
    "device_001": b"supersecretkey123",
    "device_002": b"anothersecret456",
}

def verify_data_packet(device: str, sig: str, payload: dict) -> dict | None:
    """
    Verify the cryptographic signature of an IoT data packet.

    Parameters
    ----------
    device : str
        Unique identifier of the sending IoT device.
    sig : str
        Hex-encoded cryptographic signature that accompanies the payload.
    payload : dict
        The actual data to be processed.

    Returns
    -------
    dict | None
        The original payload if the signature is valid, otherwise ``None``.

    Raises
    ------
    ConnectionError
        If the packet cannot be verified due to missing information or
        communication errors (e.g., unknown device, malformed signature).
    """
    # Basic sanity checks
    if not isinstance(device, str) or not isinstance(sig, str) or not isinstance(payload, dict):
        raise ConnectionError("Malformed packet: invalid types for device/sig/payload")

    # Retrieve the trusted secret key for this device
    try:
        secret_key = TRUSTED_DEVICE_SIGNATURES[device]
    except KeyError as exc:
        raise ConnectionError(f"Unknown device '{device}'") from exc

    # Compute the expected HMAC signature over a canonical representation of the payload
    try:
        # Convert payload to a deterministic byte string (JSON sorted keys)
        import json
        canonical_payload = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    except Exception as exc:
        raise ConnectionError("Failed to serialize payload for signature verification") from exc

    # Compute HMAC-SHA256
    expected_sig = hmac.new(secret_key, canonical_payload, hashlib.sha256).hexdigest()

    # Constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(expected_sig, sig.lower()):
        # Signature mismatch – data is untrusted
        return None

    # Signature verified; return the original payload
    return payload