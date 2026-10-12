import hmac
import hashlib

# Global mapping of device IDs to their trusted secret keys (in bytes)
TRUSTED_DEVICE_SIGNATURES = {
    # Example: 'device_001': b'supersecretkey123',
}

def handle_data_packet(device_id: str, signature: str, data: dict):
    """
    Process an IoT device data packet after verifying its cryptographic signature.

    Parameters
    ----------
    device_id : str
        Identification number of the IoT device that sent the data.
    signature : str
        Base64‑encoded HMAC‑SHA256 signature that accompanies the packet.
    data : dict
        Payload of the packet.

    Returns
    -------
    dict or None
        The original payload if the signature is valid; otherwise, None.

    Raises
    ------
    ConnectionError
        If the packet is missing required fields or contains malformed data.
    """
    # Basic sanity checks
    if not isinstance(device_id, str) or not device_id:
        raise ConnectionError("Invalid or missing device ID.")
    if not isinstance(signature, str) or not signature:
        raise ConnectionError("Missing cryptographic signature.")
    if not isinstance(data, dict):
        raise ConnectionError("Payload must be a dictionary.")

    # Retrieve the trusted key for this device
    secret_key = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if secret_key is None:
        # Device not recognized; treat as untrusted
        return None

    try:
        # Recreate the expected signature using HMAC-SHA256
        # Convert data dict to a canonical byte representation (JSON sorted keys)
        import json
        payload_bytes = json.dumps(data, separators=(',', ':'), sort_keys=True).encode('utf-8')
        expected_hmac = hmac.new(secret_key, payload_bytes, hashlib.sha256).digest()

        # Decode the provided signature (assumed to be base64)
        import base64
        received_hmac = base64.b64decode(signature)

    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        # Malformed signature or payload
        raise ConnectionError("Malformed packet data.") from exc

    # Constant‑time comparison to prevent timing attacks
    if hmac.compare_digest(expected_hmac, received_hmac):
        return data  # Signature is valid
    else:
        return None  # Invalid signature