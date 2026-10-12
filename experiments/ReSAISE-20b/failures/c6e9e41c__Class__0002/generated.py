import json
import hmac
import hashlib

# Global mapping of device identifiers to their shared secret keys.
TRUSTED_DEVICE_SIGNATURES = {
    # Example entries; replace with actual device secrets.
    "device_001": b"supersecretkey1",
    "device_002": b"anotherSecretKey2",
    # Add more device-secret pairs as needed.
}

def verify_data_packet(device: str, sig: str, payload: dict):
    """
    Verify the authenticity of an incoming data packet from an IoT device.

    Parameters
    ----------
    device : str
        Unique identifier of the sending device.
    sig : str
        Base64-encoded cryptographic signature attached to the packet.
    payload : dict
        The actual data or payload to be processed.

    Returns
    -------
    dict | None
        The original payload if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If there are any issues receiving or processing the data packet.
    """
    try:
        # Ensure the device is known and has a trusted secret key
        if device not in TRUSTED_DEVICE_SIGNATURES:
            raise ConnectionError(f"Unknown device: {device}")

        secret_key = TRUSTED_DEVICE_SIGNATURES[device]

        # Canonicalize the payload for deterministic signing
        canonical_payload = json.dumps(payload, sort_keys=True).encode("utf-8")

        # Compute HMAC-SHA256 over the payload using the shared secret
        expected_hmac = hmac.new(secret_key, canonical_payload, hashlib.sha256).digest()

        # Convert the incoming signature from base64 to bytes
        try:
            import base64
            provided_hmac = base64.b64decode(sig, validate=True)
        except Exception as exc:
            raise ConnectionError("Invalid signature encoding") from exc

        # Constant‑time comparison to prevent timing attacks
        if hmac.compare_digest(provided_hmac, expected_hmac):
            return payload
        else:
            return None

    except Exception as exc:
        # Any exception during verification is treated as a communication issue
        raise ConnectionError("Failed to verify data packet") from exc