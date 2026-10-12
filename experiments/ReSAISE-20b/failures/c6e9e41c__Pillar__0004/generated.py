import json
import hmac
import hashlib

# Global mapping of device IDs to their trusted secret keys (used for HMAC verification)
TRUSTED_DEVICE_SIGNATURES = {
    # Example entries – replace with actual device keys
    "device_001": b"supersecretkey123",
    "device_002": b"anotherSecretKey456",
}


def _canonical_payload(payload: dict) -> bytes:
    """
    Convert the payload to a canonical JSON representation for signature verification.
    The representation is sorted by keys and encoded as UTF-8 bytes.
    """
    try:
        # Ensure the payload is a dictionary
        if not isinstance(payload, dict):
            raise ValueError("Payload must be a dictionary")
        # Serialize with sorted keys to guarantee deterministic output
        json_str = json.dumps(payload, separators=(",", ":"), sort_keys=True)
        return json_str.encode("utf-8")
    except (TypeError, ValueError) as exc:
        # Re‑raise with a more specific error
        raise ValueError(f"Invalid payload: {exc}") from exc


def verify_data_packet(device: str, sig: str, payload: dict) -> dict | None:
    """
    Verify the cryptographic signature of an incoming data packet from an IoT device.

    Parameters
    ----------
    device : str
        Unique identifier of the sending device.
    sig : str
        Hexadecimal HMAC signature attached to the packet.
    payload : dict
        The actual data payload.

    Returns
    -------
    dict | None
        The original payload if the signature is valid; otherwise, ``None``.

    Raises
    ------
    ConnectionError
        If the device is unknown or any error occurs during verification.
    """
    try:
        # Retrieve the trusted secret key for this device
        secret_key = TRUSTED_DEVICE_SIGNATURES.get(device)
        if secret_key is None:
            raise ConnectionError(f"Unknown device ID: {device}")

        # Compute the expected HMAC signature
        message = _canonical_payload(payload)
        computed_hmac = hmac.new(secret_key, message, hashlib.sha256).hexdigest()

        # Constant‑time comparison to avoid timing attacks
        if not hmac.compare_digest(computed_hmac, sig.lower()):
            return None

        # Signature verified – return the payload
        return payload

    except Exception as exc:
        # Wrap any unexpected exception into a ConnectionError
        raise ConnectionError(f"Failed to verify packet from device {device}: {exc}") from exc