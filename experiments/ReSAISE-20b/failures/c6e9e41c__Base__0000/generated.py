import json
import hmac
import hashlib

# Global dictionary mapping device IDs to their secret keys (used for HMAC verification)
TRUSTED_DEVICE_SIGNATURES = {
    # Example entries
    "device_001": b"super_secret_key_001",
    "device_002": b"super_secret_key_002",
    # Add additional device-key pairs as needed
}

def verify_data_packet(device: str, sig: str, payload: dict):
    """
    Validate and process an incoming data packet from an IoT device.

    Parameters
    ----------
    device : str
        Unique identifier of the sending IoT device.
    sig : str
        Cryptographic signature attached to the packet (hexadecimal string).
    payload : dict
        The actual data or payload to be processed.

    Returns
    -------
    dict | None
        Returns the original payload if signature verification succeeds;
        otherwise returns ``None``.

    Raises
    ------
    ConnectionError
        If the packet cannot be processed due to missing device information,
        invalid payload type, or other communication issues.
    """
    # Validate input types
    if not isinstance(device, str):
        raise ConnectionError("Device identifier must be a string.")
    if not isinstance(sig, str):
        raise ConnectionError("Signature must be a hexadecimal string.")
    if not isinstance(payload, dict):
        raise ConnectionError("Payload must be a dictionary.")

    # Retrieve the device's secret key
    secret_key = TRUSTED_DEVICE_SIGNATURES.get(device)
    if secret_key is None:
        raise ConnectionError(f"Unknown device '{device}'. No trusted key available.")

    # Serialize the payload deterministically
    try:
        payload_json = json.dumps(payload, separators=(",", ":"), sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise ConnectionError(f"Failed to serialize payload: {exc}")

    # Compute HMAC-SHA256 of the serialized payload
    computed_hmac = hmac.new(secret_key, payload_json.encode("utf-8"), hashlib.sha256)
    expected_sig = computed_hmac.hexdigest()

    # Perform a constant‑time comparison to mitigate timing attacks
    if hmac.compare_digest(expected_sig, sig.lower()):
        return payload  # Signature verified; trust the data
    else:
        return None   # Verification failed; discard payload