import hmac
import hashlib

# Example trusted signatures (secret keys) per device.
# In a real deployment these would be securely stored and managed.
TRUSTED_DEVICE_SIGNATURES = {
    "device_001": b"supersecretkey1",
    "device_002": b"anothersecretkey2",
    # Add more devices as needed
}


def verify_data_packet(device: str, sig: str, payload: dict) -> dict | None:
    """
    Verify the cryptographic signature of a data packet from an IoT device.

    Parameters
    ----------
    device : str
        Unique identifier of the device that sent the packet.
    sig : str
        Base64‑encoded HMAC signature attached to the packet.
    payload : dict
        The actual data payload to be processed.

    Returns
    -------
    dict | None
        The original payload if the signature is valid; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the device is unknown or any error occurs during signature verification.
    """
    # Ensure we have a trusted key for the device
    try:
        secret_key = TRUSTED_DEVICE_SIGNATURES[device]
    except KeyError as exc:
        raise ConnectionError(f"Unknown device '{device}'.") from exc

    # Re‑compute the HMAC over a canonical representation of the payload.
    # We use JSON encoding with sorted keys to guarantee deterministic ordering.
    try:
        import json
        payload_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
    except Exception as exc:
        raise ConnectionError(f"Failed to serialize payload for device '{device}'.") from exc

    # Compute the expected HMAC (using SHA256)
    try:
        hmac_obj = hmac.new(secret_key, payload_bytes, hashlib.sha256)
        expected_sig = hmac_obj.digest()
    except Exception as exc:
        raise ConnectionError(f"Failed to compute HMAC for device '{device}'.") from exc

    # The incoming signature is expected to be base64‑encoded
    try:
        import base64
        provided_sig_bytes = base64.b64decode(sig, validate=True)
    except Exception as exc:
        # Invalid base64 data is treated as a verification failure
        return None

    # Constant‑time comparison to avoid timing attacks
    if hmac.compare_digest(expected_sig, provided_sig_bytes):
        return payload

    # Signature did not match
    return None