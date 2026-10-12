import hmac
import hashlib

# Global dictionary mapping device IDs to their secret keys (used for HMAC signatures)
TRUSTED_DEVICE_SIGNATURES = {
    # Example entries – replace with actual device secrets
    "device_001": b"supersecretkey1",
    "device_002": b"supersecretkey2",
    # Add more device secrets here
}

def process_iot_packet(device_id: str, crypt_sig: str, pkt_data: dict) -> dict | None:
    """
    Validate the HMAC signature of an IoT packet and return processed data.

    Parameters
    ----------
    device_id : str
        Unique identifier of the IoT device.
    crypt_sig : str
        Hex-encoded HMAC signature sent with the packet.
    pkt_data : dict
        Payload of the IoT packet.

    Returns
    -------
    dict | None
        Processed data if signature verification succeeds; otherwise None.

    Raises
    ------
    ConnectionError
        If the packet cannot be received successfully (e.g., missing data).
    """
    # Simulate a scenario where packet reception might fail
    if pkt_data is None:
        raise ConnectionError("Failed to receive packet data")

    # Retrieve the secret key for the device
    secret_key = TRUSTED_DEVICE_SIGNATURES.get(device_id)
    if secret_key is None:
        # Unknown device – treat as invalid
        return None

    # Compute the expected HMAC (using SHA256)
    try:
        computed_hmac = hmac.new(secret_key, msg=str(pkt_data).encode('utf-8'),
                                 digestmod=hashlib.sha256).hexdigest()
    except Exception as exc:
        # In case of unexpected errors during HMAC calculation
        raise RuntimeError(f"HMAC computation failed: {exc}") from exc

    # Use constant‑time comparison to mitigate timing attacks
    if not hmac.compare_digest(computed_hmac, crypt_sig):
        return None

    # At this point the signature is verified – perform any domain‑specific
    # processing on pkt_data here. For illustration, we simply return the data.
    processed = {
        "device_id": device_id,
        "payload": pkt_data,
        "status": "verified"
    }
    return processed